// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract farmer {

  address[] _farmers;
  string[] _farmernames;
  mapping(address=>bool) _f;

  address[] _distributors;
  string[] _distributornames;
  mapping(address=>bool) _d;

  address[] _shops;
  string[] _shopnames;
  mapping(address=>bool) _s;

  uint[] _assetid;
  address[] _assetf;
  address[] _assetd;
  address[] _assets;

  uint _id;

  address admin;

  constructor() 
  {
    _id=0;
    admin=msg.sender;
  }

  modifier onlyAdmin() {
    require(admin==msg.sender);
    _;
  }

  function addFarmer(address f_wallet,string memory f_name) onlyAdmin public {
    require(!_f[f_wallet]);
    _farmers.push(f_wallet);
    _farmernames.push(f_name);
    _f[f_wallet]=true;
  }

  function viewFarmer() public view returns(address[] memory,string[] memory) {
    return(_farmers,_farmernames);
  }

  function addDistributor(address d_wallet,string memory d_name) onlyAdmin public {
    require(!_d[d_wallet]);
    _distributors.push(d_wallet);
    _distributornames.push(d_name);
    _d[d_wallet]=true;
  }

  function viewDistributor() public view returns(address[] memory, string[] memory) {
    return(_distributors,_distributornames);                                                                
  }

  function addShop(address s_wallet, string memory s_name) onlyAdmin public {
    require(!_s[s_wallet]);
    _shops.push(s_wallet);
    _shopnames.push(s_name);
    _s[s_wallet]=true;
  }

  function viewShop() public view returns(address[] memory,string[] memory) {
    return(_shops,_shopnames);
  }

  function addAsset(address f_wallet) public {
    require(_f[f_wallet]);
    _id+=1;
    _assetid.push(_id);
    _assetf.push(f_wallet);
    _assetd.push(f_wallet);
    _assets.push(f_wallet);
  }
  function viewAsset() public view returns(uint[] memory,address[] memory,address[] memory,address[] memory) {
    return(_assetid,_assetf,_assetd,_assets);
  }

  function sellAssetToDistributor(uint assetid,address f_wallet,address d_wallet) public returns(bool){
    uint i;
    require(_f[f_wallet]);
    require(_d[d_wallet]);
    for(i=0;i<_assetid.length;i++){
      if(assetid==_assetid[i] && _assetf[i] ==f_wallet){
        _assetd[i]=d_wallet;
        return true;
      }
    }
    return false;
  }
  function sellAssetToShop(uint assetid,address d_wallet, address s_wallet) public returns(bool) {
    uint i;
    require(_d[d_wallet]);
    require(_s[s_wallet]);
    for(i=0;i<_assetid.length;i++){
      if(assetid==_assetid[i] && _assetd[i]==d_wallet){
        _assets[i]=s_wallet;
        return true;
      }
    }
    return false;
  }
}
