from bigip.ltm.core.irules import IRules, IRule
from bigip.ltm.core.nodes import Nodes, Node
from bigip.ltm.core.pools import Pools, Pool
from bigip.ltm.core.vips import Vips, Vip
from bigip.ltm.core.monitors import Monitors, Monitor
from bigip.ltm.core.profiles import Profiles, Profile


if __name__ == "__main__":
### GET - Multiple Devices ########################################

    # bigip1 = IRule("bigip1")
    # bigip1._get_names()

    # bigip1 = Nodes("bigip1")
    # bigip1._get_names()

    # bigip1 = Node("bigip1")
    # bigip1._get_config()

    # bigip1 = Pool("bigip1")
    # bigip1._get_config("test_pool_1")

    # bigip1 = Vips("bigip1")
    # bigip1._profiles_get_names()
 
    # bigip1 = Vip("bigip1")
    # bigip1._exists("vip_1")


    # bigip1 = Monitors("bigip1")
    # bigip1._get_config()

    # bigip1 = Monitor("bigip1")
    # bigip1._exists("tcp")

### Create - Multiple Devices #####################################

    # bigip1 = IRules("bigip1")
    # bigip1._create()
    # bigip1._update()

    # bigip1 = Monitors("bigip1")
    # bigip1._create()
    # bigip1._update()

    # bigip1 = Profiles("bigip1")
    # bigip1._create()

    # bigip1 = Nodes("bigip1")
    # bigip1._create()
    # bigip1._update()

    # bigip1 = Pools("bigip1")
    # bigip1._create()
    # bigip1._update()

    # bigip1 = Vips("bigip1")
    # bigip1._create()
    # bigip1._update()


### Delate - Multiple Devices #####################################

    # bigip1 = Vips("bigip1")
    # bigip1._delete_all()

    # bigip1 = Pools("bigip1")
    # bigip1._delete_all()

    # bigip1 = Nodes("bigip1")
    # bigip1._delete_all()

    # bigip1 = Profiles("bigip1")
    # bigip1._delete_all()

    # bigip1 = Monitors("bigip1")
    # bigip1._delete_all()

    # bigip1 = IRules("bigip1")
    # bigip1._delete_all()


### Declare - Multiple Devices ################

    # bigip1 = IRules("bigip1")
    # bigip1._declare()

    # bigip1 = Nodes("bigip1")
    # bigip1._declare()

    # bigip1 = Pools("bigip1")
    # bigip1._declare() 

    # bigip1 = Vips("bigip1")
    # bigip1._declare()


### IRules ####################################

    # bigip1 = IRules("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._create()
    # bigip1._update()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()
    # bigip1._declare()

    # bigip1 = IRule("bigip1")
    # bigip1._create("api_pool_selection")
    # bigip1._update("api_pool_selection")
    # bigip1._delete("rule1")


### Monitors ####################################

    # bigip1 = Monitors("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._create()
    # bigip1._update()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()  
    # bigip1._declare()

    # bigip1 = Monitor("bigip1")
    # bigip1._get_config("http_monitor_1")
    # bigip1._create("http_monitor_1")
    # bigip1._delete("http_monitor_1")
    # bigip1._exists("http_monitor_1")


### Profiles #####################################

    # bigip1 = Profiles("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._create()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()
    # bigip1._declare()


    # bigip1 = Profile("bigip1")
    # bigip1._get_config("http_prof_2")
    # bigip1._create("http_prof_1")
    # bigip1._delete("http_prof_1")
    # bigip1._exists("http_prof_2")


### Nodes #####################################

    # bigip1 = Nodes("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._create()
    # bigip1._update()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()
    # bigip1._declare()

    # bigip1 = Node("bigip1")
    # bigip1._get_config("node_1")
    # bigip1._create("node_1")
    # bigip1._update("node_1")
    # bigip1._delete("node_1")
    # bigip1._exists("node_1")
    # bigip1._ip_exists("10.1.1.1")

### Pools #####################################

    # bigip1 = Pools("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._create()
    # bigip1._update()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()
    # bigip1._declare()

    # bigip1 = Pool("bigip1")
    # bigip1._get_config("pool_1")
    # bigip1._create("pool_1")
    # bigip1._update("pool_1")
    # bigip1._delete("pool_1")
    # bigip1._exists("pool_1")


### Vips ######################################

    # bigip1 = Vips("bigip1")
    # bigip1._get_names()
    # bigip1._get_config()
    # bigip1._get_members()
    # bigip1._create()
    # bigip1._update()
    # bigip1._delete_not_sot()
    # bigip1._delete_all()
    # bigip1._declare()

    # bigip1 = Vip("bigip1")
    # bigip1._get_names()
    # bigip1._get_config("vip_1")
    # bigip1._create("vip_1")
    # bigip1._update("vip_1")
    # bigip1._delete("vip_1")
    # bigip1._exists("vip_1")
    # print(bigip1._call_method("vip_1").name)