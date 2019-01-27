# Udacity Project 4 Item Catalog

## Used Programs
* Vagrant
* Oracle VirtualBox
* Vagrant 3.5.2


## Setup
* Clone repo locally
* Run vagrant up inside the vagrant folder
* Vagrant ssh to connect to the virtual machine
* Inside the VM, cd to /vagrant/catalog
* Run python3 views.py
* In your browser open localhost:5000

* A prebuilt database is in the repo, but if you need to rebuild it from scratch, you can run createCatalog.py

Link structure is setup as the below:
localhost:5000/catalog/[Category Name]/[Item Name]
/edit and /delete can be added to the end of the link while logged in to access those features
/create can be used in the place of where catalog is to add an item to the category (without an item name)

### Planned Future Features
* Facebook and email login

Note: Item descriptions were pulled from semi-relevant Wikipedia articles