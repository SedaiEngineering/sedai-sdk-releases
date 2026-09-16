from datetime import datetime, timedelta, timezone

from sedai import optimizations

# get optimizations by resource id
resource_id = "resource_id"
endtime = datetime.now(tz=timezone.utc)
starttime = endtime - timedelta(weeks=2)

opts = optimizations.get_resource_optimizations(
    resource_id=resource_id, starttime=starttime, endtime=endtime
)
for opt in sorted(opts, key=lambda x: x.optimization_time, reverse=True):
    print("Optimized at: ", opt.optimization_time)
    print("Pre Hourly Cost: ", opt.pre_hourly_cost)
    print("Post Hourly Cost: ", opt.post_hourly_cost)
    print("Cost Savings Hourly: ", opt.cost_change_per_hour)
    print("---")
