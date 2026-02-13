from app.Settings import Settings
from langchain_community.utilities import SearxSearchWrapper

def test_searchxng_connection():
    try:
        s = SearxSearchWrapper(searx_host=Settings.SEARCHXNG)
        s.run("what is a large language model?")
        if s.results:
            return "SearchXNG connection successful"
    except Exception as e:
        return f"SearchXNG connection failed: {str(e)}"
