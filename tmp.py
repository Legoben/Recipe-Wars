foodtypes = [{"n":"American","id":"american"},{"n":"American: Southern","id":"american-southern"},{"n":"Asian","id":"asian"},{"n":"French","id":"french"},{"n":"Indian","id":"indian"},{"n":"Italian","id":"italian"},{"n":"Mexican","id":"mexican"},{"n":"Other","id":"n-a"}]
str = "["
for f in foodtypes:
    str += "'"+f['id']+"', "
print(str)