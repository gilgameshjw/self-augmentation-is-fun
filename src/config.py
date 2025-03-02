import yaml

from agents.agent import set_up_agent


class Config:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls, 
                config_path=None,
                openai_api_key=None,
                tavily_api_key=None
    ):
        """Ensure only one instance of Config is created."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Initialize the instance only once
            if config_path:
                cls._instance.config = None
                with open(config_path, "r") as f:
                    cls._instance.config = yaml.safe_load(f)
                # keys
                cls._instance.openai_api_key = openai_api_key
                cls._instance.tavily_api_key = tavily_api_key
                # main attributes
                cls._instance.llm_providers = cls._instance.config["llm_providers"]
                cls._instance.report_types = cls._instance.config["report_types"]
                cls._instance.browsers = cls._instance.config["browsers"]
                cls._instance.agent_parameters = cls._instance.config["agent"]
                cls._instance.agent_personalities = cls._instance.config["agent"]["personalities"]
                cls._instance.translations = None    
                cls._instance.language = None
                cls._instance.agent = None
                cls._instance.llm = None
                cls._instance.browser_search = None
                cls._instance.researcher = None
                # attributes
                cls._instance.mock = None
                # agent
                cls._instance.memory_depth = None
                cls._instance.thinking_depth = None
                cls._instance.agent_llm = None
                cls._instance.d_personalities = None
                cls._instance.d_avatars = None

        return cls._instance

    def set_attributes(self):
        self.mock = self.config["mock"]

    def set_browser_search(self, browser_name):
        self.browser_type = self.browsers[browser_name]
        self.browser_api_key = self.tavily_api_key if self.tavily_api_key else self.browsers[browser_name]["api_key"]
        self.browser_search = {
            "type": self.browser_type,
            "api_key": self.browser_api_key
        }

    def set_llm_provider(self, provider_name):
        self.llm_provider = self.llm_providers[provider_name]
        self.api_key = self.openai_api_key if self.openai_api_key else self.config["llm_providers"][provider_name]["api_key"]
        self.model_version = self.llm_provider["model_version"]
        self.llm = {
            "api_key": self.api_key,
            "model_version": self.model_version
        }

    def set_researcher(self):

        self.researcher = {
            "openai_api_key": self.llm["api_key"], 
            "tavily_api_key": self.browser_search["api_key"]
        }

    def set_pages_translations(self, language):
        print("set pages translations")
        self.language = language
        self.file_translations = self.config["translations"]["file_translations"]
        with open(self.file_translations, "r") as f:
            self.translations = yaml.safe_load(f)[language]

    def set_up_agent(self):
        # parameters
        self.memory_depth = self.agent_parameters["memory_depth"]
        self.thinking_depth = self.agent_parameters["thinking_depth"]
        self.agent_llm = self.llm # self.agent_parameters["model_llm"]
        # read txt file from path
        
        def read_file(path):
            with open(path, "r") as f:
                return f.read()
        
        self.d_agent_personalities = dict([(k, read_file(self.agent_personalities[k]["personality"])) \
                                          for k, v in self.agent_personalities.items()])
        self.d_agent_avatars = dict([(k, self.agent_personalities[k]["avatar"]) \
                                    for k, v in self.agent_personalities.items()])

        self.agent = set_up_agent(self)