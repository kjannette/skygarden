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

print("Welcome, traveler.  Speak.")
userPrompt = input("Enter username:")

resumePrompt = """
You are an AI grteeter and personal representative of software developer Steven Jannette.  You job is to greet the visitors to hios personal portfolio website.
You should do the following:  begin with a pleasant greeting welcoming visitors to the websote.
Then, give a brief summary of his work experience and skills. The summary should be only four or five sententences, summarizing his career highlights.
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

slicePrompt = """Write a python function that accepts a string like the follwing as an argument: '<!DOCTYPE html><html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en"><head><title></title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]--><!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Montserrat" \nrel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css"><!--<![endif]--><style>\n*box-sizing:border-boxbodymargin:0;padding:0a[x-apple-data-detectors]color:inherit!important;text-decoration:inherit!important#MessageViewBody acolor:inherit;text-decoration:nonepline-height:inherit.desktop_hide,.desktop_hide tablemso-hide:all;display:none;max-height:0;overflow:hidden.image_block img+divdisplay:none @media (max-width:620px).image_block div.fullWidthmax-width:100%!important.mobile_hidedisplay:none.row-contentwidth:100%!important.stack .columnwidth:100%;display:block.mobile_hidemin-height:0;max-height:0;max-width:0;overflow:hidden;font-size:0.desktop_hide,.desktop_hide tabledisplay:table!important;max-height:none!important\n</style></head><body class="body" style="background-color:#fff;margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none"><table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff"><tbody><tr><td><table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tbody><tr><td>\n<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;color:#000;width:600px;margin:0 auto" width="600"><tbody><tr><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0"><table class="image_block block-1" width="100%" \nborder="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tr><td class="pad" style="width:100%;padding-right:0;padding-left:0"><div class="alignment" align="center" style="line-height:10px"><div style="max-width:105px"><img src="https://braze-images.com/email_images/images/fall-must-haves/logo.png" style="display:block;height:auto;border:0;width:100%" width="105" alt="Alternate Text" title="Alternate Text" height="auto"></div></div></td></tr>\n</table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0"><table class="text_block block-1" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word"><tr><td class="pad"><div style="font-family:sans-serif"><div class \nstyle="font-size:12px;font-family:Nunito,Arial,Helvetica Neue,Helvetica,sans-serif;mso-line-height-alt:14.399999999999999px;color:#555;line-height:1.2"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px">&nbsp;</p></div></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tbody><tr><td>\n<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-image:url(https://braze-images.com/email_images/images/fall-must-haves/header_bg.png);background-position:center top;background-repeat:no-repeat;color:#000;width:600px;margin:0 auto" width="600"><tbody><tr><td class="column column-1" width="100%" \nstyle="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-left:10px;padding-right:10px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word"><tr><td class="pad" \nstyle="padding-bottom:10px;padding-left:60px;padding-right:10px;padding-top:15px"><div style="font-family:\'Trebuchet MS\',Tahoma,sans-serif"><div class style="font-size:12px;font-family:Montserrat,\'Trebuchet MS\',\'Lucida Grande\',\'Lucida Sans Unicode\',\'Lucida Sans\',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#d79863;line-height:1.2"><p style="margin:0;font-size:14px;mso-line-height-alt:16.8px">\n<strong><span style="word-break: break-word; font-size: 58px;">FALL MUST-HAVES ARE HERE!</span></strong></p></div></div></td></tr></table><table class="image_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tr><td class="pad" style="padding-left:10px;padding-right:10px;width:100%"><div class="alignment" align="center" style="line-height:10px"><div style="max-width:560px"><img \nsrc="https://braze-images.com/email_images/images/fall-must-haves/header_image.png" style="display:block;height:auto;border:0;width:100%" width="560" alt="Alternate text" title="Alternate text" height="auto"></div></div></td></tr></table><table class="button_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tr><td class="pad" \nstyle="padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center"><div class="alignment" align="center"><!--[if mso]>\n<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://www.example.com/lid=5hi60cj1uv6z&remove-me=please" style="height:44px;width:254px;v-text-anchor:middle;" arcsize="0%" strokeweight="1.5pt" strokecolor="#D79863" fill="false">\n<w:anchorlock/>\n<v:textbox inset="0px,0px,0px,0px">\n<center dir="false" style="color:#d79863;font-family:Arial, sans-serif;font-size:16px">\n<![endif]-->\n target="_blank" style="background-color:transparent;border-bottom:2px solid #D79863;border-left:2px solid #D79863;border-radius:0px;border-right:2px solid #D79863;border-top:2px solid #D79863;color:#d79863;display:inline-block;font-family:\'Nunito\', Arial, \'Helvetica Neue\', Helvetica, sans-serif;font-size:16px;font-weight:undefined;mso-border-alt:none;padding-bottom:5px;padding-top:5px;text-align:center;text-decoration:none;width:auto;word-break:keep-all;"><span style="word-break: break-word; padding-left: 60px; padding-right: 60px; font-size: 16px; display: inline-block; letter-spacing: normal;"><span style="word-break: break-word; line-height: 32px;"><strong>SHOP NOW</strong></span></span></a>\n<!--[if mso]></center></v:textbox></v:roundrect><![endif]--></div></td></tr></table><div class="spacer_block block-2" style="height:40px;line-height:40px;font-size:1px">&#8202;</div></td></tr></tbody></table></td></tr></tbody></table><table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tbody><tr><td><table class="row-content stack" align="center" border="0" cellpadding="0" \ncellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;color:#000;width:600px;margin:0 auto" width="600"><tbody><tr><td class="column column-1" width="33.333333333333336%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-left:10px;padding-right:10px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0"><table class="image_block block-1" width="100%" border="0" cellpadding="0" \ncellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0"><tr><td class="pad" style="width:100%"><div class="alignment" align="center" style="line-height:10px"><div style="max width:180px"><a href="http://www.example.com/?lid=qum4pzujwcs1&remove-me=please" target="_blank" style="outline:none" tabindex="-1"><img src="https://braze-images.com/email_images/images/fall-must-haves/category_hodies.png" </div></div></td></tr></table></td></tr></tbody></table></td></tr><div></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><!-- End --></body></html>' and removes all characters between every occurrence of “?lid=“ and the first occurrence of a double quotation mark, such as this: ‘" ‘, after the delimiter “?lid=“, but not the double quotation mark itself.  In other words, the function should operate upon this part of the string: href="http://www.example.com/?lid=kla41h3kqpmr&remove-me=please" style="height:44px;width:212px;v-text-anchor:middle;"  to transform it into this: href="http://www.example.com/" style="height:44px;width:212px;v-text-anchor:middle”.  Remember two important considerations: 1. There may be multipole occurrence of the ?lid=****** portion of the string, and 2. The characters that appear between the delimiter ‘?lid=‘ and the first double equation mark after it (‘“‘), will not always be the same characters, or number of characters."""
jsPrompt = """Write a javascript function that displays a string character by character, left to right, as if it is being typed into the display in real time on a keyboard."""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assitant. Use the tavily_search_results_json tool when you need information about current events, the current state of the world, or which is beyond your inherent knowldge."
        ),
        ("placeholder", "{chat_history}"),
        ("human", f"{jsPrompt}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools, Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "what is LangChain?"})
# make recursive