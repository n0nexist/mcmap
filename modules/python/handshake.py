import os

# obtains the result
# of joining a server
def getHandshakeResult(host,port,protocol):
    result = os.popen(f"java -jar modules/java/n0nejoin.jar {host} {port} {protocol}").read().strip()
    if "Exception" in result:
        result = "\033[31mJava Error"
    return result