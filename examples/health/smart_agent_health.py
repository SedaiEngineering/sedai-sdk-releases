from sedai.health import smart_agent_health

def get_agent_health():
    smart_agents = smart_agent_health.get_health_info()
    if not smart_agents:
        print("No smart agents found")
    else:
        for agent in smart_agents:
            print()
            print()
            print("Account name: ", agent.account_name)
            print("Account Id: ", agent.account_id)
            print("Healthy: ", agent.is_healthy)
            print("Agent Available:", agent.is_agent_available)
            print("Live : ", agent.live_connection_status)
            print("Connection Type: ", agent.connection_type)
            print("Agent version: ", agent.version)
            print("Desired version: ", agent.desired_version)
            print("Last supported version: ", agent.last_supported_version)
            print("Upgrade needed: ", agent.upgrade_needed)
            print("Spec controller version:", agent.spec_controller_version)
            print("Last checked: ", agent.latest_health_check_time)
            for job in agent.job_health_list or []:
                print()
                print("Job Id: ",job.job_id)
                print("Job status: ", job.job_status)
                print("Status: ", job.is_healthy)
                print("Last check: ", job.health_check_time)
                print("Last healthy on: ", job.last_healthy_on)
                print("Last refreshed on: ", job.last_refreshed_on)
                print("Message: ", job.message)
            for stat in agent.message_stats or []:
                print()
                print("Action : ", stat.action)
                print("Average execution time: ", stat.average_execution_time_millis)
                print("Total executions: ", stat.total_executions)
                print("Successful executions: ", stat.successful_executions)
                print("Failed executions: ", stat.failed_executions)

if __name__ == '__main__':
    get_agent_health()