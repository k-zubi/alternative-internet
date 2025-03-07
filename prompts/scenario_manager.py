import os
import json
from typing import Dict, List, Optional


class ScenarioTemplate:
    """Class to manage scenario description templates."""

    def __init__(self, name: str, description: str, scenario: str):
        """
        Initialize a scenario template.
        
        Args:
            name: Unique identifier for the template
            description: Human-readable description of this scenario
            scenario: The full scenario description text
        """
        self.name = name
        self.description = description
        self.scenario = scenario

    @classmethod
    def from_dict(cls, data: Dict) -> "ScenarioTemplate":
        """
        Create a ScenarioTemplate from a dictionary.
        
        Args:
            data: Dictionary with template data
            
        Returns:
            ScenarioTemplate instance
        """
        return cls(
            name=data["name"],
            description=data["description"],
            scenario=data["scenario"]
        )

    def to_dict(self) -> Dict:
        """
        Convert template to dictionary for serialization.
        
        Returns:
            Dictionary representation of the template
        """
        return {
            "name": self.name,
            "description": self.description,
            "scenario": self.scenario
        }


class ScenarioManager:
    """Manager for loading and accessing scenario templates."""

    def __init__(self, templates_dir: str = "prompts"):
        """
        Initialize the scenario manager.
        
        Args:
            templates_dir: Directory containing scenario template files
        """
        self.templates_dir = templates_dir
        self.scenarios: Dict[str, ScenarioTemplate] = {}
        self._load_scenarios()

    def _load_scenarios(self) -> None:
        """Load all scenario templates from the templates directory."""
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Load default scenarios if no files exist
        if not any(f.endswith('.json') for f in os.listdir(self.templates_dir)):
            self._create_default_scenarios()
            
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.templates_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        scenario_data = json.load(f)
                        scenario = ScenarioTemplate.from_dict(scenario_data)
                        self.scenarios[scenario.name] = scenario
                except Exception as e:
                    print(f"Error loading scenario {filename}: {e}")

    def _create_default_scenarios(self) -> None:
        """Create default scenario templates."""
        # EtherWeave scenario (the original)
        etherweave = ScenarioTemplate(
            name="etherweave",
            description="Ancient magical internet powered by alchemy and arcane forces",
            scenario="""Imagine a world where the Internet was not born from silicon and code but from the ancient, arcane machinations of alchemists in the late Renaissance. In this alternate timeline, mystics uncovered the secret of the "EtherWeave"—a luminous network spun from enchanted fibers and quantum spells that intertwined the minds of scholars, artists, and adventurers across Europe and beyond. Instead of servers, colossal magical conduits known as Arcanet Pillars powered communication, channeling not only information but also the very essence of human creativity, passion, and memory. Navigating the EtherWeave felt akin to embarking on a fantastical voyage, where each website was a living tapestry of surreal landscapes, animated by whispering sprites and drifting runes. The boundaries between science and sorcery blurred as citizens consulted visualized prophecies, traded mystic relics, and even summoned intelligent digital phantoms to debate philosophy and predict the future—a virtual realm where every click was a spell and every message a magical incantation setting the stage for a renaissance of the human spirit."""
        )
        
        # Cyberpunk scenario
        cyberpunk = ScenarioTemplate(
            name="cyberpunk",
            description="Dystopian internet dominated by megacorporations and digital rebellion",
            scenario="""In 2077, after the Corporate Wars, six megacorporations divided the remnants of the global network. This fractured internet, known as "NeoNet," is a digital battleground where corporate enclaves control verified citizens through neural interfaces, while the outcasts—digital nomads and rogue AI collectives—roam the unpatrolled dataflows of the Deep Grid. Information is the most valuable currency, traded in black market data-havens and protected by militarized ICE protocols that can trigger seizures or brain death in unauthorized users. Advertisements materialize unbidden in users' peripheral vision, personalized by invasive biometric monitoring. Those wealthy enough maintain digital avatars that persist autonomously in VR social clubs even while they sleep. Meanwhile, resistance networks mask communications as innocuous entertainment streams, sending coded messages through popular neural-dance recordings and augmented reality games. Corporations offer citizens the illusion of freedom while monitoring every digital footprint, using predictive algorithms to eliminate dissenters before they act—an internet built not for connection, but for control."""
        )
        
        # Solarpunk scenario
        solarpunk = ScenarioTemplate(
            name="solarpunk",
            description="Optimistic eco-futurist internet focused on sustainability and community",
            scenario="""In the early 2030s, after the Great Decentralization Movement, the internet transformed into the "Flourish Network"—a constellation of community-owned mesh networks powered by renewable energy. Data centers, once massive energy sinks, have been replaced by distributed microcenters housed in community gardens, rooftop solar arrays, and wind-powered co-ops. The new internet operates on a "Prosocial Protocol" that allocates bandwidth based on community benefit rather than profit potential. Urban farming collectives share realtime soil and climate data through tactile interfaces woven from recycled e-waste and biodegradable polymers. Instead of algorithms optimizing for engagement, the Attention Cooperative stewards digital spaces that enhance genuine human connection. Users navigate the network through immersive "groves"—collaborative spaces where information grows like living gardens, tended by community librarians and knowledge gardeners. Hyperlocal exchange platforms have replaced global e-commerce, with physical location and resource sharing embedded in the digital architecture. The barriers between online and offline have dissolved as augmented reality overlays show the ecological impact of physical actions and suggest community-sourced alternatives—an internet devoted not to extraction but to regeneration."""
        )

        # Retrofuturist scenario
        retrofuturist = ScenarioTemplate(
            name="retrofuturist",
            description="1950s-style retrofuturist internet with atomic age aesthetics",
            scenario="""Welcome to the "Atomnet," the gleaming electronic marvel of 1957! After the breakthrough of the Consolidated Vacuum Tube Computer (CVTC) by Bell Laboratories in 1951, home terminals became the pride of every modern American household. Your family's Atomnet Console, with its polished mahogany cabinet and glowing vacuum tubes, connects to Regional Information Centers through dedicated copper telephone trunk lines. Navigating information is a tactile experience—turning brass dials and pressing Bakelite buttons to tune into "frequencies" rather than web addresses. Housewives access the Electronic Home Advisory System for recipe cards and domestic science bulletins, while businessmen consult the Statistical Business Tabulation Grid. Children enjoy educational programming from the Academic Television Council, transmitting directly to the console's built-in radar screen. For just 35 cents per query, users can pose questions to EMERALD, the Electrical Mathematical Engine for Research and Logical Deduction, receiving printed responses on special atomic-age stationery. Television-Telephone convergence allows families to speak face-to-face with relatives in other Atomnet-equipped cities during designated connection periods. The system operates with perfect atomic precision, immune to the communist infiltration that threatens other communication networks—a technological testament to American ingenuity and optimism."""
        )
        
        # Save default scenarios
        self._save_scenario(etherweave)
        self._save_scenario(cyberpunk)
        self._save_scenario(solarpunk)
        self._save_scenario(retrofuturist)

    def _save_scenario(self, scenario: ScenarioTemplate) -> None:
        """
        Save a scenario template to disk.
        
        Args:
            scenario: ScenarioTemplate to save
        """
        file_path = os.path.join(self.templates_dir, f"{scenario.name}.json")
        with open(file_path, 'w') as f:
            json.dump(scenario.to_dict(), f, indent=2)
        self.scenarios[scenario.name] = scenario

    def get_scenario(self, name: str) -> Optional[ScenarioTemplate]:
        """
        Get a scenario by name.
        
        Args:
            name: Scenario name
            
        Returns:
            ScenarioTemplate or None if not found
        """
        return self.scenarios.get(name)

    def add_scenario(self, scenario: ScenarioTemplate) -> None:
        """
        Add a new scenario template.
        
        Args:
            scenario: ScenarioTemplate to add
        """
        self._save_scenario(scenario)

    def get_all_scenarios(self) -> List[ScenarioTemplate]:
        """
        Get all available scenarios.
        
        Returns:
            List of all scenarios
        """
        return list(self.scenarios.values())
        
    def get_scenario_names(self) -> List[str]:
        """
        Get names of all available scenarios.
        
        Returns:
            List of scenario names
        """
        return list(self.scenarios.keys())