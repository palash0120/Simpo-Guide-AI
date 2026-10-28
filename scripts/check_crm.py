
from app.crm.tools import search_leads



if __name__ == "__main__":
    print(search_leads.name)          # search_leads
    print(search_leads.description)   # the docstring text the LLM reads
    print(search_leads.args)          # the JSON schema of the arguments

    print(search_leads.invoke({"keyword": "Akshaya"}))
    print(search_leads.invoke({"days": 7, "limit": 3}))
