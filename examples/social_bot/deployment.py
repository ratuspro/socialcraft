from socialcraft import AgentManager
import pathlib
import os
import random

names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle", "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma", "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Frank", "Debra", "Alexander", "Rachel", "Raymond", "Catherine", "Patrick", "Carolyn", "Jack", "Janet", "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane", "Jose", "Virginia", "Adam", "Julie", "Henry", "Joyce", "Nathan", "Victoria", "Douglas", "Olivia", "Zachary", "Kelly", "Peter", "Christina", "Kyle", "Lauren", "Walter", "Joan", "Ethan", "Evelyn", "Jeremy", "Judith", "Harold", "Megan", "Keith", "Cheryl", "Christian", "Andrea", "Roger", "Hannah", "Noah", "Martha", "Gerald", "Jacqueline", "Carl", "Frances", "Terry", "Gloria", "Sean", "Ann", "Austin", "Teresa", "Arthur", "Kathryn", "Lawrence", "Sara", "Jesse", "Janice", "Dylan", "Jean", "Bryan", "Alice", "Joe", "Madison", "Jordan", "Doris", "Billy", "Abigail", "Bruce", "Julia", "Albert", "Judy", "Willie", "Grace", "Gabriel", "Denise", "Logan", "Amber", "Alan", "Marilyn", "Juan", "Beverly", "Wayne", "Danielle", "Roy", "Theresa", "Ralph", "Sophia", "Randy", "Marie", "Eugene", "Diana", "Vincent", "Brittany", "Russell", "Natalie", "Elijah", "Isabella", "Louis", "Charlotte", "Bobby", "Rose", "Philip", "Alexis", "Johnny", "Kayla"]

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal",
                           minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)),
                        "blueprint/")

    agent_blueprint = manager.generate_blueprint(name="social_bot_template", agent_source_path=str(path))


    all_agents = manager.get_all_agents()

    for old_agent in all_agents:
        old_agent.kill()

    # SETTINGS
    NUMBER_OF_AGENTS = 6
    NUMBER_OF_GROUPS = 2

    # BOOTSTRAP AGENTS
    agents=[]
    
    for i in range(0,NUMBER_OF_AGENTS):
        agents.append({
            "name": random.choices(names)[0],
            "social_group": random.choices(range(NUMBER_OF_GROUPS))[0] 
        })

    # Create Agent
    for agent in agents:
        old_agent = manager.get_agent(agent["name"])
 
        if old_agent is not None:
            old_agent.kill()

        new_agent = manager.create_agent(name=agent["name"], blueprint = agent_blueprint, custom_envs={"SOCIAL_GROUP": agent["social_group"]})
        new_agent.deploy()