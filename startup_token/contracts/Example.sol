// SPDX-License-Identifier: CC-BY-SA-4.0

// Version of Solidity compiler this program was written for
pragma solidity >=0.6.4;

contract Owned {
  address payable owner;

  // Contract constructor: set owner
  constructor() {
    owner = msg.sender;
  }

  // Access control modifier
  modifier onlyOwner {
    require(msg.sender == owner, "Only the contract owner can call this function");
    _;
  }

  // Contract destructor
  function destroy() public onlyOwner {
    selfdestruct(owner);
  }
}

contract Faucet is Owned {

  uint withdraw_limit;
  event Withdrawal(address indexed to, uint amount);
  event Deposit(address indexed from, uint amount);

  constructor(uint _limit) {
    withdraw_limit = _limit;
  }

  // Accept any incoming amount
  receive() external payable {
    emit Deposit(msg.sender, msg.value);
  }

  // Give out ether to anyone who asks
  function withdraw(uint withdraw_amount) public {
    // Limit withdrawal amount
    require(withdraw_amount <= withdraw_limit, "Too many ether requested.");

    require(address(this).balance >= withdraw_amount,"Insufficient balance in faucet for withdrawal request");

    // Send the amount to the address that requested it
    msg.sender.transfer(withdraw_amount);

    emit Withdrawal(msg.sender, withdraw_amount);
  }
}