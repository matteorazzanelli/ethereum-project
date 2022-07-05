// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/NotaryAct.sol";

contract TestNotaryAct is NotaryContract{
  // The address of the NotaryContract contract to be tested
  NotaryContract act = NotaryContract(DeployedAddresses.NotaryContract());

  ////////////////////////////////////////////////////////////////
  function testInitialSupplyUsingDeployedContract() public {
    uint totalSupply_expected = 0;
    Assert.equal(act.totalSupply(), uint(totalSupply_expected), "Owner should have 0 NTT initially");
    Assert.equal(act.minPeriodOfDeadline_(), 1 weeks, "Minimum period of deadline shoud be 1 week");
  }

  ////////////////////////////////////////////////////////////////
  function testnewContract() public {
    address payable buyer = payable(address(0xCa30bd31a8f9C962Ed0A7e5D506EfC487663ad77));
    address payable seller = payable(address(0x63BF670c9c54B51aa9832dD3AC667528e4eF39A6));
    act.newContract(buyer, seller, "Prova di description", 100, 1 weeks);
    uint num = uint(act.numContract_());

    
    Assert.equal(uint(num), uint(1), "Num contract should be 1");
    Assert.equal(act.getTitleDeed(1).buyer,buyer,"Buyer not correct.");
    Assert.equal(act.getTitleDeed(1).seller,seller,"Seller not correct.");
  }

  ////////////////////////////////////////////////////////////////
  function testnewPayment() public {
    // ...
  }

  ////////////////////////////////////////////////////////////////
  function testcheckGoalReached() public {
    // ...
  }

  ////////////////////////////////////////////////////////////////
  function testdeletedNotaryAct() public {
    // ...
  }

}