# Python Blockchain
by: Adriel

This is a sample project demonstrating the core ideas of the blockchain.


### What Is a Blockchain?
- A blockchain is a distributed ledger that is shared among the nodes/computers on a network. 
- A blockchain stores information electronically in digital format. 
- Blockchains are best known for their crucial role in cryptocurrency systems, such as Bitcoin, for maintaining a secure and decentralized record of transactions.


### How this project is structured
- python-blockchain
  - chain_sample.json
  - single_node
    - blockchain.py
    - server.py
   - multi_node
      - blockchain.py
      - server.py
  - venv
  - .gitignore
  - LICENCE
  - README.md
  - requirements.txt


### Setting up the project
1. pull the project: `git clone https://github.com/lonestarx1/python-blockchain.git`
2. go into the pulled directory: `cd python-blockchain`
3. create a virtual environment: `python3 -m venv venv`
4. activate the virtual environment:
    - windows cmd: `venv\Scripts\activate`
    - windows git-bash:  `source venv/Scripts/activate`
    - mac & linux: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Start the server: `python single_node/server.py`

- this will start a development server at your local IP address port 5000.
- this server can be reached by any other machine on the same network.
- you can control the mining difficulty by passing a parameter when starting the server: `python single_node/server.py 3`
  - I recommend trying 3,4 and 5
  - If no value is passed, the default difficulty is 4


You can interact with the blockchain by calling the available endpoints. below are the samples of endpoints available and the response they return

#### Getting the current chain
![chain](https://user-images.githubusercontent.com/52321271/145651080-094b9f4c-459a-42de-a178-3dce8fcf9462.JPG)

#### Posting a transaction
![post transaction](https://user-images.githubusercontent.com/52321271/145651112-5c44dd0a-a9db-4444-9baf-969831c58855.JPG)

#### Getting pending transactions
![transactions](https://user-images.githubusercontent.com/52321271/145651255-5617c2de-ebae-4205-b0dc-4f35f137527b.JPG)

#### Mining a block from pending transactions
![mine](https://user-images.githubusercontent.com/52321271/145651127-238fbfdb-0c58-45bc-a204-8be57787ccd3.JPG)

#### Checking the balance of a particular address
![balance](https://user-images.githubusercontent.com/52321271/145651131-3d217200-5cd3-4d57-af78-96054c73c1c8.JPG)


