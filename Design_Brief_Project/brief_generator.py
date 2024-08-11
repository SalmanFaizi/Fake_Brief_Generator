def get_current_datetime():
    """
    Get the current date and time.
    
    Returns:
    str: Current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    from datetime import datetime

    # Get the current date and time
    current_datetime = datetime.now()
    
    # Format the date and time as 'YYYY-MM-DD HH:MM:SS'
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    return datetime_str


def generate_brief(brief_type, domain):

    import os
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq


    os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
    chat = ChatGroq(temperature=0.5, model_name="mixtral-8x7b-32768")
    # Example usage
    current_datetime = get_current_datetime()

    system=f"Generate a design brief for a {brief_type} in the {domain} industry. Include a company name, company description, design requirements, and a deadline(The deadline must be According to the requirement and an experienced person would take to complete in days and it should be  after the current date and time {current_datetime})."
    
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    res = chain.invoke({"text": f'Create realistic design brief for the {brief_type} and {domain}.'})



    print("***********************************************************")
    # Your brief generation logic here
    return res.content

# design_type=input("Enter design type eg. logo,bilboard,packaging etc. ")
# Industry=input("Enter Industry eg. Tech,Education,Food etc ")

# result=generate_brief(design_type,Industry)
# print(result)
