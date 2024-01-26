from flask import Flask,render_template,request,redirect;
import json
from web3 import Web3,HTTPProvider;

def connect_with_farmer(wallet):
    blockchain="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain))
    print('Server Connected')
    if wallet==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet

    with open("../build/contracts/farmer.json") as f:
        artifact=json.load(f)
        abi=artifact['abi']
        address=artifact['networks']['5777']['address']

    contract=web3.eth.contract(abi=abi,address=address)
    print('Contract Selected')
    return contract,web3

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/farmer')
def farmer():
    contract,web3=connect_with_farmer(0)
    _farmers,_farmernames=contract.functions.viewFarmer().call()
    print(_farmers,_farmernames)
    l=len(_farmers)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_farmernames[i])
        dummy.append(_farmers[i])
        data.append(dummy)
    return render_template('farmer.html',num=l,data=data)

@app.route('/distributor')
def distributor():
    contract,web3=connect_with_farmer(0)
    _distributors,_distributornames=contract.functions.viewDistributor().call()
    print(_distributors,_distributornames)
    l=len(_distributors)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_distributornames[i])
        dummy.append(_distributors[i])
        data.append(dummy)
    return render_template('distributor.html',num=l,data=data)

@app.route('/shop')
def shop():
    contract,web3=connect_with_farmer(0)
    _shops,_shopnames=contract.functions.viewShop().call()
    print(_shops,_shopnames)
    l=len(_shops)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_shopnames[i])
        dummy.append(_shops[i])
        data.append(dummy)
    return render_template('shop.html',num=l,data=data)

@app.route('/asset')
def asset():
    contract,web3 = connect_with_farmer(0)
    _assetid, _assetf, _assetd, _assets = contract.functions.viewAsset().call()
    print(_assetid, _assetf, _assetd, _assets)
    _farmers, _farmernames = contract.functions.viewFarmer().call()
    _distributors, _distributornames = contract.functions.viewDistributor().call()
    _shops, _shopnames = contract.functions.viewShop().call()
    print(_farmers, _farmernames)
    print(_distributors, _distributornames)
    print(_shops, _shopnames)
    l = len(_assetid)
    data = []
    for i in range(l):
        dummy = []
        dummy.append(_assetid[i])
        findex = _farmers.index(_assetf[i])
        dummy.append(_farmernames[findex])
        if _assetf[i]==_assetd[i]:
            dummy.append("not dispatched")
        else:
            dindex=_distributors.index(_assetd[i])
            dummy.append(_distributornames[dindex])
        if _assetf[i]!=_assetd[i] and _assetf[i]==_assets[i]:
            dummy.append("In Warehouse")
        elif _assetf[i]!=_assets[i]:
            sindex=_shops.index(_assets[i])
            dummy.append(_shopnames[sindex])
        else:
            dummy.append("not dispatched")
        data.append(dummy)
    return render_template('asset.html',num=l,data=data)



@app.route('/indexdata',methods=['post'])
def indexdata():
    assetid=int(request.form['assetid'])
    print(assetid)
    contract,web3=connect_with_farmer(0)
    _assetid,_assetf,_assetd,_assets=contract.functions.viewAsset().call()
    print(_assetid,_assetf,_assetd,_assets)
    if assetid in _assetid:
        aindex=_assetid.index(assetid)
        assetf=_assetf[aindex]
        assetd=_assetd[aindex]
        assets=_assets[aindex]
        _farmers,_farmernames=contract.functions.viewFarmer().call()
        _distributors,_distributornames=contract.functions.viewDistributor().call()
        _shops,_shopnames=contract.functions.viewShop().call()
        findex=_farmers.index(assetf)
        assetf1=_farmernames[findex]
        if assetf==assetd:
            assetd1="fake"
        else:
            dindex=_distributors.index(assetd)
            assetd1=_distributornames[dindex]
        if assetf==assets:
            assets1="fake"
        else:
            sindex=_shops.index(assets)
            assets1=_shopnames[sindex]
    else:
        assetf1="Fake"
        assetd1="Fake"
        assets1="Fake"


    return render_template('index.html',id=assetid,assetf=assetf1,assetd=assetd1,assets=assets1)

@app.route('/farmerdata',methods=['post'])
def farmerdata():
    f_wallet=request.form['f_wallet']
    f_name=request.form['f_name']
    print(f_wallet,f_name)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addFarmer(f_wallet,f_name).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/farmer')

@app.route('/distributordata',methods=['post'])
def distributordata():
    d_wallet=request.form['d_wallet']
    d_name=request.form['d_name']
    print(d_wallet,d_name)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addDistributor(d_wallet,d_name).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/distributor')

@app.route('/shopdata',methods=['post'])
def shopdata():
    s_wallet=request.form['s_wallet']
    s_name=request.form['s_name']
    print(s_wallet,s_name)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addShop(s_wallet,s_name).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/shop')

@app.route('/assetdata',methods=['post'])
def assetdata():
    f_wallet=request.form['f_wallet']
    print(f_wallet)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addAsset(f_wallet).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/asset')

@app.route('/sellasset')
def sellasset():
    return render_template('sellasset.html')

@app.route('/sellassettodistributor',methods=['post'])
def sellassettodistributor():
    f_wallet=request.form['fwallet']
    d_wallet=request.form['dwallet']
    assetid=request.form['assetid']
    print(f_wallet,d_wallet,assetid)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.sellAssetToDistributor(int(assetid),f_wallet,d_wallet).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/asset')

@app.route('/sellassettoshop',methods=['post'])
def sellassettoshop():
    dwallet1=request.form['dwallet1']
    s_wallet=request.form['swallet']
    assetid=request.form['assetid1']
    print(dwallet1,s_wallet,assetid)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.sellAssetToShop(int(assetid),dwallet1,s_wallet).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect('/asset')




if __name__ =="__main__":
    app.run('127.0.0.1',5001,debug=True)
