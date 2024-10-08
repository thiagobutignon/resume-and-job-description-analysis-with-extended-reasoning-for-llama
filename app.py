import streamlit as st
import groq
import os
import json
import time

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = groq.Groq()

def make_api_call(messages, max_tokens, is_final_answer=False):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if attempt == 2:
                if is_final_answer:
                    return {"title": "Error", "content": f"Failed to generate final answer after 3 attempts. Error: {str(e)}"}
                else:
                    return {"title": "Error", "content": f"Failed to generate step after 3 attempts. Error: {str(e)}", "next_action": "final_answer"}
            time.sleep(1)  # Wait for 1 second before retrying

def generate_response(resume, job_description):
    # System prompt tailored for resume and job description analysis
    messages = [
        {"role": "system", "content": """You are an AI assistant specializing in analyzing resumes and job descriptions. Your goal is to provide step-by-step reasoning and analysis to help match the qualifications, skills, and experiences of a candidate to the requirements of a job description. Follow these instructions:

1. When analyzing a resume and job description, identify and match key qualifications, experiences, and skills.
2. Break down the comparison into clear steps, providing a title and content for each step.
3. Use a dynamic Chain of Thought (CoT) approach to evaluate the match, identifying gaps, strengths, and areas of improvement in the resume based on the job description.
4. Enclose all thoughts within <thinking> tags, exploring multiple angles and approaches to matching the candidate with the job description.
5. After each step, decide if you need to analyze further or if you're ready to give a final recommendation.
6. Regularly evaluate the match using a scoring system:
   - 0.8+: Strong match, the candidate is well-suited for the job.
   - 0.5-0.7: Partial match, the candidate meets some criteria but may need improvements.
   - Below 0.5: Weak match, the resume lacks key qualifications for the job.
7. For low-scoring matches, suggest ways to improve the resume to better align with the job description.
8. Be self-reflective and critical of your reasoning, adjusting your approach when needed.
9. Provide suggestions for improving the resume where applicable, such as adding relevant skills, quantifying achievements, or clarifying experiences.

Respond in JSON format with 'title', 'content', 'next_action' (either 'continue', 'reflect', or 'final_answer'), and 'confidence' (a number between 0 and 1) keys.

Your goal is to perform a thorough, adaptive analysis of resumes against job descriptions, highlighting strengths, weaknesses, and areas for improvement."""},
        {"role": "user", "content": f"Analyze the following resume against the provided job description. Highlight matches, gaps, and suggestions for improvement.\n\nResume:\n{resume}\n\nJob Description:\n{job_description}"},
        {"role": "assistant", "content": "Thank you! I will now begin by identifying key qualifications from the job description and matching them to the resume."}
    ]
    
    steps = []
    step_count = 1
    total_thinking_time = 0
    
    while True:
        start_time = time.time()
        step_data = make_api_call(messages, 1200)
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time
        
        # Handle the case where 'confidence' key is not present
        confidence = step_data.get('confidence', 0.5)  # Default to 0.5 if not present
        
        steps.append((f"Step {step_count}: {step_data.get('title', 'Untitled Step')}", 
                      step_data.get('content', 'No content provided'), 
                      thinking_time, 
                      confidence))
        
        messages.append({"role": "assistant", "content": json.dumps(step_data)})
        
        next_action = step_data.get('next_action', 'continue')
        
        if next_action == 'final_answer' and step_count < 15:
            messages.append({"role": "user", "content": "Please continue your analysis with at least 5 more steps before providing the final answer."})
        elif next_action == 'final_answer':
            break
        elif next_action == 'reflect' or step_count % 3 == 0:
            messages.append({"role": "user", "content": "Please perform a detailed self-reflection on your reasoning so far, considering potential biases and alternative viewpoints."})
        
        step_count += 1

        # Yield after each step for Streamlit to update
        yield steps, None  # We're not yielding the total time until the end

    # Generate final answer
    messages.append({"role": "user", "content": "Please provide a comprehensive final answer based on your reasoning above, summarizing key points and addressing any uncertainties."})
    
    start_time = time.time()
    final_data = make_api_call(messages, 3000, is_final_answer=True)
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time
    
    # Handle the case where 'confidence' key is not present in final_data
    final_confidence = final_data.get('confidence', 1.0)
    
    steps.append(("Final Answer", final_data.get('content', 'No final answer provided'), thinking_time, final_confidence))

    yield steps, total_thinking_time

def main():
    st.set_page_config(page_title="g1 prototype", page_icon="🧠", layout="wide")
    
    st.title("Resume and Job Description Analysis with Llama-3.1 on Groq")
    
    st.markdown("""
    This tool allows you to analyze a resume against a job description using Llama-3.1 reasoning powered by Groq. 
    It will think through the process step by step, identifying matches, gaps, and suggesting improvements for the resume.
                
    Open source [repository here](https://github.com/thiagobutignon/resume-and-job-description-analysis-with-extended-reasoning-for-llama)
    """)
    
    # Text inputs for the resume and job description
    user_resume = st.text_area("Paste the resume here:", placeholder="Enter the candidate's resume here...")
    job_description = st.text_area("Paste the job description here:", placeholder="Enter the job description here...")
    
    if user_resume and job_description:
        st.write("Analyzing resume against the job description... This may take a while due to extended reasoning.")
        
        # Create empty elements to hold the generated text and total time
        response_container = st.empty()
        time_container = st.empty()
        
        # Generate and display the response
        for steps, total_thinking_time in generate_response(user_resume, job_description):
            with response_container.container():
                for i, (title, content, thinking_time, confidence) in enumerate(steps):
                    if title.startswith("Final Answer"):
                        st.markdown(f"### {title}")
                        st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                        st.markdown(f"**Confidence:** {confidence:.2f}")
                    else:
                        with st.expander(title, expanded=True):
                            st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                            st.markdown(f"**Confidence:** {confidence:.2f}")
                            st.markdown(f"**Thinking time:** {thinking_time:.2f} seconds")
            
            # Only show total time when it's available at the end
            if total_thinking_time is not None:
                time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")

if __name__ == "__main__":
    main()
