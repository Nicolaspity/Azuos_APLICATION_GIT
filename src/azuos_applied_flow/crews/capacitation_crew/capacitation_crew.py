from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

''''''


@CrewBase
class CapacitationCrew():
    """CapacitationCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def instructor(self) -> Agent:
        return Agent(
            config=self.agents_config['instructor'], # type: ignore[index]
            verbose=True
        )

    @task
    def topic_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['topic_writing_task'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CapacitationCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
