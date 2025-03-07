from lm.base_lm_client import BaseLMClient
from lm.cerebras_lm_client import CerebrasLMClient
from lm.openai_lm_client import OpenAILMClient
from prompts.scenario_manager import ScenarioManager, ScenarioTemplate


class Chat:

    def __init__(self, scenario_description: str = None, scenario_name: str = None):
        self.lm_client: BaseLMClient = CerebrasLMClient()
        # self.lm_client: BaseLMClient = OpenAILMClient()
        self.scenario_manager = ScenarioManager()
        
        # Handle scenario selection
        if scenario_name:
            scenario_template = self.scenario_manager.get_scenario(scenario_name)
            if scenario_template:
                scenario_description = scenario_template.scenario
            else:
                print(f"Scenario '{scenario_name}' not found. Using default scenario.")
                default_scenario = self.scenario_manager.get_scenario("etherweave")
                scenario_description = default_scenario.scenario if default_scenario else "A fictional alternative internet"
        elif not scenario_description:
            # If no scenario provided, use the default
            default_scenario = self.scenario_manager.get_scenario("etherweave")
            scenario_description = default_scenario.scenario if default_scenario else "A fictional alternative internet"
        
        self.scenario_description = scenario_description
        
        # Initialize conversation with system prompt
        self.conversation: list[dict[str, str]] = [
            {
                "role": "system",
                "content": self.get_system_prompt(scenario_description=scenario_description)
            }
        ]

    def browse_to_page(self, path: str) -> str:
        self.conversation.append(
            {
                "role": "user",
                "content": f"""The user has browsed to the following path: "{path}".
Generate an HTML page as instructed for this path based on the scenario given. Remember to only respond with the HTML site and no additional comment whatsoever."""
            }
        )
        response: str = self.lm_client.do_chat_completion(messages=self.conversation)
        self.conversation.append(
            {
                "role": "assistant",
                "content": response
            }
        )
        print("Generated page.")
        return response
    
    def get_available_scenarios(self):
        """Get list of all available scenarios with descriptions."""
        scenarios = []
        for scenario in self.scenario_manager.get_all_scenarios():
            scenarios.append({
                "name": scenario.name,
                "description": scenario.description
            })
        return scenarios
        
    def add_custom_scenario(self, name: str, description: str, scenario: str):
        """Add a new custom scenario."""
        template = ScenarioTemplate(name=name, description=description, scenario=scenario)
        self.scenario_manager.add_scenario(template)
        return template
        
    def change_scenario(self, scenario_name: str = None, scenario_description: str = None):
        """Change the current scenario."""
        if scenario_name:
            scenario_template = self.scenario_manager.get_scenario(scenario_name)
            if scenario_template:
                scenario_description = scenario_template.scenario
            else:
                print(f"Scenario '{scenario_name}' not found.")
                return False
        
        if scenario_description:
            self.scenario_description = scenario_description
            # Reset conversation with new scenario
            self.conversation = [
                {
                    "role": "system",
                    "content": self.get_system_prompt(scenario_description=scenario_description)
                }
            ]
            return True
        return False

    @staticmethod
    def get_system_prompt(scenario_description: str) -> str:
        return f"""You are a highly creative and motivated HTML generator of an alternative internet of a fictional scenario.

You are given a path that the internet user has navigated to and your job is to dynamically generate a very lengthy, extremely detailed and fully working HTML page with in-line CSS and without any JavaScript fitting the given fictional scenario.
The HTML page should use hyperlinks to other pages that are structured like "/tld/domain/page/subpage/..." like e.g. "/com/news/main". Important: Do not use double slashes at the beginning, only a single one.
The pages should not have any mention or indication that they are alternative or fictional scenarios or otherwise directly speak to the user and really give the indication that the user is browsing this alternative scenario.
Make the pages as detailed as possible, containing lots of content, hyperlinks etc.
If you want to include image, do so by using <img> tags with detailed, descriptive filenames containing 5-10 words separated by hyphens (e.g., "ancient-mystic-portal-with-glowing-blue-runes.jpg").

VERY IMPORTANT: ALWAYS respond ONLY with the HTML code and NO additional comment and NO markdown code brackets, just begin with "<!DOCTYPE html>".

This is the fictional scenario for the alternative internet:
```
{scenario_description}
```"""