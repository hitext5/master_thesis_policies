## Policy Example of the policy languages rego, sentinel, casbin and polar

Example policy where a hairdryer and fan are already powered by a solar panel and a charger is also to be plugged in. Tests are written so that they pass. For example, if an electronic device is increased to 70, the test fails. All files are named the same, in casbin_example -> casbin_app -> casbin_test is the pytest for casbin. For opa, oso and sentinel also this order. The other files are the policies, which are needed for the evaluation.

# To Bootstrap the Project

Install packages: pip install -r requirements.txt

Download the rego exe from here:  
https://www.openpolicyagent.org/docs/latest/#running-opa

Download the sentinel exe from here:
https://docs.hashicorp.com/sentinel/downloads

# Policy languages pages

https://casbin.org/docs/overview
https://www.osohq.com/docs
https://www.openpolicyagent.org/docs/latest/
https://docs.hashicorp.com/sentinel/writing/imports
