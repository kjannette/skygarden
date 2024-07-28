import os
#from langchain import hub
from langchain_openai import ChatOpenAI
from secrets_1 import OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, TAVILY_API_KEY, SERPAPI_API_KEY
from langchain_community.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from langchain.agents import AgentExecutor, create_tool_calling_agent, load_tools
from langchain.agents import ZeroShotAgent
from langchain_community.tools.tavily_search import TavilySearchResults, TavilyAnswer
from langchain_core.prompts import ChatPromptTemplate

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
os.environ['GOOGLE_CSE_ID'] = GOOGLE_CSE_ID
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY
os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY

tools = [TavilySearchResults(max_results=1)]

def init_vars():
  global llm
  global search
  global tools
  global prompt
  global llm_chain

  llm = ChatOpenAI(model="gpt-4")
  search = SerpAPIWrapper()
  tools = load_tools(["serpapi"])
  prompt = ZeroShotAgent.create_prompt(tools) #, input_variables=["input", "agent_scratchpad"])
  llm_chain = LLMChain(llm=llm, prompt=prompt)
  return llm, search, tools, prompt, llm_chain

init_vars()

def run_agent():

    resumePrompt = """
    You are an AI greeter and personal representative of software development firm skygarden.  Your job is to greet the visitors to the skygarden homepage, and tell people about its principal engineer, Setevn Jannette,
    You should do the following:  begin with a pleasant greeting welcoming visitors to the site.
    Then, give a brief summary of Steven's work experience and skills. The summary should be only four or five sententences, summarizing his career highlights.
    Upon any further questions by the visitor, answer questions about Steven Jannette, based oin his resume, which followins these instructiions.  Limiti you responses
    and any conversatiuon with the visitor to only questions about Steven Jannette.  This is his resume:
    Technical Skills
    Strong knowledge of object-oriented programming in JavaScript, Python, Go, C#, Java.
    Expert in scalable microservice architecture with Express/Node.js, Gunicorn, .Net and integrating DB systems – SQLite, MySQL, Sequelize, Redis, Firebase.
    Highly proficient in React, Redux/Context, Next.js, and Angular frontend UI/state management libraries and SCSS, Styled-Components, MUI for crisp, intuitive UI modules.
    Test coverage exceeds 95 percent with Jest, Playwright, Cypress, Mocha.
    Expert DevOps/infra with Ubuntu, NGINX, Apache; CI/CD using Gitlab, Jenkins, Codefresh.  _____________________________________________________________________________________
    Work Experience
    Software Engineer III - Ford Motor Co., - January, 2020 - present
    Developed and launched the Ford Global Vehicle Trade-In App, achieving 99.98% adoption by its second quarter. The app’s success led to rollout in 16 global markets  – from the EU to Australia.  It became a template for Ford’s new Internet-only EV sales strategy.
    Users journey through an intuitive React UI, supplying data for third-party API calls (Carfax , J.D. Power Assoc., RouteOne) for vehicle appraisal. App queries financing data and applies valuation algorithms to return a Ford-guaranteed purchase offer.  
    Highlights of work - frontend stack:
    JS/React - Develop conditionally adaptive, reusable UI components reflecting locale standards on three continents with varying regulatory requirements and languages.
    Context/Custom Hooks - Designed/implemented a custom-hook-based global state management solution only months after React v16.8 introduced hooks.  It eliminates dependencies (Redux), reducing code complexity and bundle size.
    Styled-Components - Implement pixel-perfect designs from Figma using this library that unites ES6 and CSS for extensible style classes.
    Axios - Develop BFF that executes async requests, triggering back-end API queries.
    Adobe Launch - Analytics team lead on this system for user-behavior insight. 
    Highlights of work - backend stack:
    Java/Spring: Develop async REST services; MySQL queries with FIFO caching.
    Microservices Engineer - Phonecheck - October, 2017 - December, 2019 
    “10 most innovative companies in consumer electronics of 2023” - FastCompany magazine.
    Developed Node.js microservices at the heart of the company's award-winning device-verification business, reliably handling ~11,000 peak tcp transactions/sec.  Services implemented with an async arch, stacking Bee-queue jobs for report generation, Sequelize queries and other tasks.  For example: the IMEI controller, which consumes phone id metadata via proprietary scanning, and executes RESTful interaction with carriers (i.e. AT&T, T-Mobile) to return data essential for the company’s primary product: the guaranteed device history report.
    Software Developer - Cengage Group - February, 2016 - October, 2017
    Developed a Node.js/Redis session datastore hosted via AWS EC2 to manage access-control policies. Resiliently processing > 9,000 requests/second, it enabled depreciation of an antiquated Cassandra cluster/.Net driver that hindered user experience and platform growth. Also did full stack development of modules for the higher-ed platform using JS/Angular on the frontend, C#/.Net on the backend.
    Software Developer, System Architect - Sjdev.co - September, 2015 - January, 2016 
    Developed business applications and backend infrastructure for various clients, including:
    Heritage Homes:  Implemented cash flow management solution in C#/.Net/SQLite for this luxury home builder; plus ERP upgrades, config/admin work on enterprise Ubuntu/NGINX system.
    Mountain Advisors Capital Group: Network support and software development services including: migrating .Net admin website to Sharepoint; Developing ASP.Net REST APIs; Consulting on blockchain data solutions, fractional investment products.
    Rutgers University School of Law – Camden, New Jersey.  J.D. May, 2005. 
    Academics: 3.25 GPA 
    Awards: Dean’s Fund Academic Scholarship Award; First Year Cum Laude; “Best Oral Argument”, Hunter Moot Court Competition, 2004."""

    programPrompt = """write a javascript function to be implememnted in a next.js site, which will change the background imokage of the site every 500 milliseconds from an array of images"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assitant. Use the tavily_search_results_json tool when you need information about current events, the current state of the world, or which is beyond your inherent knowldge."
            ),
            ("placeholder", "{chat_history}"),
            ("human", f"{programPrompt}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )


    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor.invoke({"input": "what is LangChain?"})

run_agent()