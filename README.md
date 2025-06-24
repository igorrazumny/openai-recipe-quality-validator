**🧪 OpenAI Healthcare Recipe Quality Validator**

This Streamlit app audits healthcare manufacturing recipes using OpenAI GPT-4o.  
After analysis, it generates a downloadable PDF report with findings and suggestions.

🚀 Features

- Upload JSON or CSV recipe files  
- Analyze structure, completeness, and formatting  
- Get a downloadable PDF audit report  

⚙️ Setup

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
