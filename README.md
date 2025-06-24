<h2>🧪 OpenAI Healthcare Recipe Quality Validator</h2>

This Streamlit app audits healthcare manufacturing recipes using OpenAI GPT-4o.  
After analysis, it generates a downloadable PDF report with findings and suggestions.

<h3>🚀 Features</h3>

- Upload JSON or CSV recipe files  
- Choose entry limit and OpenAI model (<code>gpt-4o</code> or <code>gpt-3.5-turbo</code>)  
- Analyze structure, completeness, and formatting  
- Get a downloadable PDF audit report  

<h3>⚙️ Setup</h3>

<pre>
git clone https://github.com/your-username/openai-recipe-quality-validator.git
cd openai-recipe-quality-validator
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt --break-system-packages
echo "OPENAI_API_KEY=sk-..." > .env
streamlit run src/app.py
</pre>

<blockquote>
<b>⚠️ This is a portfolio demonstration project built with mock data only.</b><br>
It is not affiliated with any employer, client, or production system.<br>
No confidential or proprietary information is included.
</blockquote>
