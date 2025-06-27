from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import yaml
import os


@CrewBase
class ContentCrew():
    """Azuos crew"""
    
    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config['reader'], # type: ignore[index]
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def form_interpretation_task(self) -> Task:
        return Task(
            config=self.tasks_config['form_interpretation_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.pdf'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AzuosCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
