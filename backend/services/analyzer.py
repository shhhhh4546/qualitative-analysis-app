import os
import json
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Determine which provider to use
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface").lower()

if LLM_PROVIDER == "openai":
    from openai import OpenAI
elif LLM_PROVIDER == "huggingface":
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        import torch
    except ImportError:
        print("Warning: Hugging Face transformers not installed. Install with: pip install transformers torch accelerate")
        LLM_PROVIDER = None

class ConversationAnalyzer:
    def __init__(self):
        self.provider = LLM_PROVIDER
        
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables. Set LLM_PROVIDER=openai and provide OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
            self.hf_model = None
            self.hf_tokenizer = None
            self.pipeline = None
            
        elif self.provider == "huggingface":
            # Load Hugging Face model
            import torch
            model_name = os.getenv("HUGGINGFACE_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print(f"Loading Hugging Face model: {model_name} on {device}")
            
            try:
                # Use pipeline for easier text generation
                self.pipeline = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=0 if device == "cuda" else -1,
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                    trust_remote_code=True,
                    model_kwargs={"attn_implementation": "eager"}  # Fix for compatibility
                )
                self.model_name = model_name
                print(f"Model {model_name} loaded successfully!")
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                print("Falling back to GPT-2...")
                # Fallback to a smaller, more stable model
                try:
                    self.pipeline = pipeline(
                        "text-generation",
                        model="gpt2",
                        device=-1,
                        model_kwargs={"pad_token_id": 50256}
                    )
                    self.model_name = "gpt2"
                    print("Using GPT-2 as fallback")
                except Exception as fallback_error:
                    raise ValueError(f"Could not load any Hugging Face model. Error: {fallback_error}")
            
            self.client = None
            self.model = None
        else:
            raise ValueError(f"Invalid LLM_PROVIDER: {self.provider}. Use 'openai' or 'huggingface'")
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Extract JSON from text, handling cases where model adds extra text"""
        # Try to find JSON object in the text
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # If no JSON found, try parsing the whole text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    
    def _analyze_with_openai(self, transcript: str) -> Dict:
        """Analyze using OpenAI"""
        prompt = f"""Analyze the following customer conversation transcript and extract key insights. 
Return a JSON object with the following structure:
{{
    "pain_points": [{{"point": "description", "severity": "high/medium/low"}}],
    "media_consumption": [{{"name": "media source", "type": "podcast/blog/social/etc"}}],
    "compelling_points": [{{"point": "what made them interested", "category": "feature/benefit/use_case"}}],
    "summary": "brief 2-3 sentence summary of the conversation"
}}

Focus on:
- Pain points: What problems, challenges, or frustrations did the customer mention?
- Media consumption: What podcasts, blogs, social media, newsletters, or other media did they mention consuming or following?
- Compelling points: What features, benefits, or aspects of the product/service seemed to interest or excite them?

Transcript:
{transcript[:8000]}

Return ONLY valid JSON, no additional text."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at analyzing customer conversations and extracting actionable insights. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    
    def _analyze_with_huggingface(self, transcript: str) -> Dict:
        """Analyze using Hugging Face model"""
        # Create a detailed prompt
        system_prompt = """You are an expert at analyzing customer conversations and extracting actionable insights. 
Always return valid JSON without any additional text or explanation."""

        user_prompt = f"""Analyze this customer conversation and return a JSON object with:
{{
    "pain_points": [{{"point": "description", "severity": "high/medium/low"}}],
    "media_consumption": [{{"name": "media source", "type": "podcast/blog/social/etc"}}],
    "compelling_points": [{{"point": "what made them interested", "category": "feature/benefit/use_case"}}],
    "summary": "brief 2-3 sentence summary"
}}

Focus on:
- Pain points: Problems, challenges, frustrations mentioned
- Media consumption: Podcasts, blogs, social media, newsletters mentioned
- Compelling points: Features, benefits, aspects that interested them

Conversation:
{transcript[:4000]}

Return ONLY the JSON object:"""

        # Format prompt based on model type
        if "chat" in self.model_name.lower() or "tinyllama" in self.model_name.lower():
            # Chat-based models (TinyLlama, etc.)
            full_prompt = f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_prompt}<|end|>\n<|assistant|>\n"
        elif "instruct" in self.model_name.lower() or "phi" in self.model_name.lower():
            # Instruction-tuned models (Phi-3, etc.)
            full_prompt = f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_prompt}<|end|>\n<|assistant|>\n"
        elif "mistral" in self.model_name.lower() or "mixtral" in self.model_name.lower():
            full_prompt = f"<s>[INST] {system_prompt}\n\n{user_prompt} [/INST]"
        else:
            # Generic format (GPT-2, etc.)
            full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nJSON Response:\n"

        try:
            # Generate response with compatibility fixes
            generation_kwargs = {
                "max_new_tokens": 800,
                "temperature": 0.3,
                "do_sample": True,
                "top_p": 0.95,
                "return_full_text": False,
                "truncation": True,
            }
            
            # Add pad_token_id if available
            if hasattr(self.pipeline.tokenizer, 'pad_token_id') and self.pipeline.tokenizer.pad_token_id is not None:
                generation_kwargs["pad_token_id"] = self.pipeline.tokenizer.pad_token_id
            elif hasattr(self.pipeline.tokenizer, 'eos_token_id'):
                generation_kwargs["pad_token_id"] = self.pipeline.tokenizer.eos_token_id
            
            outputs = self.pipeline(full_prompt, **generation_kwargs)
            
            generated_text = outputs[0]["generated_text"]
            
            # Extract JSON from response
            result = self._extract_json_from_text(generated_text)
            
            if result is None:
                # If JSON extraction failed, try to construct basic structure
                return {
                    "pain_points": [],
                    "media_consumption": [],
                    "compelling_points": [],
                    "summary": generated_text[:500] if generated_text else "Analysis completed"
                }
            
            return result
            
        except Exception as e:
            print(f"Error in Hugging Face generation: {e}")
            # Return fallback structure
            return {
                "pain_points": [],
                "media_consumption": [],
                "compelling_points": [],
                "summary": f"Error during analysis: {str(e)}"
            }
    
    def analyze(self, transcript: str) -> Dict:
        """
        Analyze a conversation transcript and extract:
        - Pain points
        - Media consumption
        - Compelling points
        """
        if not transcript or len(transcript.strip()) < 50:
            return {
                "pain_points": [],
                "media_consumption": [],
                "compelling_points": [],
                "summary": "Transcript too short or empty",
                "confidence_score": 0.0
            }
        
        try:
            # Use appropriate provider
            if self.provider == "openai":
                result = self._analyze_with_openai(transcript)
            elif self.provider == "huggingface":
                result = self._analyze_with_huggingface(transcript)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            # Ensure all required fields exist
            analysis_result = {
                "pain_points": result.get("pain_points", []),
                "media_consumption": result.get("media_consumption", []),
                "compelling_points": result.get("compelling_points", []),
                "summary": result.get("summary", "Analysis completed"),
                "confidence_score": 0.85  # Default confidence
            }
            
            # Calculate confidence based on extracted data
            extracted_items = (
                len(analysis_result["pain_points"]) +
                len(analysis_result["media_consumption"]) +
                len(analysis_result["compelling_points"])
            )
            
            if extracted_items > 0:
                analysis_result["confidence_score"] = min(0.95, 0.7 + (extracted_items * 0.05))
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            return {
                "pain_points": [],
                "media_consumption": [],
                "compelling_points": [],
                "summary": f"Error parsing analysis: {str(e)}",
                "confidence_score": 0.0
            }
        except Exception as e:
            # Fallback for any other errors
            return {
                "pain_points": [],
                "media_consumption": [],
                "compelling_points": [],
                "summary": f"Analysis error: {str(e)}",
                "confidence_score": 0.0
            }
    
    def analyze_batch(self, transcripts: List[str]) -> List[Dict]:
        """Analyze multiple transcripts"""
        results = []
        for transcript in transcripts:
            results.append(self.analyze(transcript))
        return results
