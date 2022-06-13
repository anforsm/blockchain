from blockchain import Blockchain
import json

main = Blockchain()

main.mine()
main.mine()
main.mine()
print(json.dumps(main.serialize(), indent=4))
# main.mine()
