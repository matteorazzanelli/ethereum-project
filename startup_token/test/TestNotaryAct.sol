// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/NotaryAct.sol";

contract TestNotaryAct is NotaryContract{
  // The address of the NotaryContract contract to be tested
  NotaryContract act = NotaryContract(DeployedAddresses.NotaryContract());
  uint public initialBalance = 1 ether; // or any other value
  uint amount = 100;
  address payable buyer = payable(address(0x528Be592Ef3F81D85a703a9933C67AEd4f585518));
  address payable seller = payable(address(0x7d5B76B730334f2042eB2d400ACb0D4bFe2b36b5));

  event Balance(address indexed from, uint amount);
  event User(address user);

  ////////////////////////////////////////////////////////////////
  function testInitialSupplyUsingDeployedContract() public {
    uint totalSupply_expected = 0;
    Assert.equal(act.totalSupply(), uint(totalSupply_expected), "Owner should have 0 NTT initially");
    Assert.equal(act.minPeriodOfDeadline_(), 1 weeks, "Minimum period of deadline shoud be 1 week");
  }

  ////////////////////////////////////////////////////////////////
  function testnewContract() public {
    act.newContract(buyer, seller, "Prova di description", amount, block.timestamp + 2 weeks);
    uint num = uint(act.numContract_());
    Assert.equal(uint(num), uint(1), "Num contract should be 1");
    Assert.equal(act.getBuyer(0),buyer,"Buyer not correct.");
    Assert.equal(act.getSeller(0),seller,"Seller not correct.");
  }

  ////////////////////////////////////////////////////////////////
  function testnewPayment() public {
    act.newPayment{value: 50 wei}(0);
    Assert.equal(act.getTitleDeed(0).amount_for_now, 50, "Amount does not correspond.");
    Assert.equal(act.getTitleDeed(0).completed, false, "Act not finished.");
  }

  ////////////////////////////////////////////////////////////////
  function testcheckGoalReached() public {
    act.newPayment{value: 50 wei}(0);
    Assert.equal(act.getTitleDeed(0).completed, true, "Act should be completed.");
    Assert.equal(act.balanceOf(buyer), 1001 wei, "Buyer does not have the right number of token.");
  }

  ////////////////////////////////////////////////////////////////
  function testdeletedNotaryAct() public {
    act.newContract(buyer, seller, "Prova di description", amount, block.timestamp + 2 weeks);
    act.newPayment{value: 50 wei}(1); // from this.address to contract (no token)
    act.deletedNotaryAct(1);
    emit Balance(buyer, act.balanceOf(buyer)); // 1001 wei
    emit Balance(buyer, ERC20.balanceOf(buyer)); // 0 wei
    emit Balance(buyer, buyer.balance); // 100 ether
    Assert.equal(act.balanceOf(buyer), 1001 wei, "2.");
    Assert.equal(ERC20.balanceOf(buyer), 0 wei, "3.");
  }

}