// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/NotaryAct.sol";

contract TestNotaryAct {
  // The address of the NotaryContract contract to be tested
  NotaryContract act = NotaryContract(DeployedAddresses.NotaryContract());

  ////////////////////////////////////////////////////////////////
  function testInitialSupplyUsingDeployedContract() public {
    uint totalSupply_expected = 0;
    Assert.equal(uint(act.totalSupply()), uint(totalSupply_expected), "Owner should have 0 NTT initially");
  }

  ////////////////////////////////////////////////////////////////
  function testnewContract() public {
    //act.newContract(address[0], address[1], "Prova di description", 100, 1 weeks)
    uint num = uint(act.numContract_());
    Assert.equal(uint(num), uint(0), "Num contract should be 1");
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


    

//   // The id of the pet that will be used for testing
//   uint expectedPetId = 8;

//   // The expected owner of adopted pet is this contract
//   address expectedAdopter = address(this);

//   // Testing the adopt() function
//   function testUserCanAdoptPet() public {
//     uint returnedId = adoption.adopt(expectedPetId);

//     Assert.equal(returnedId, expectedPetId, "Adoption of the expected pet should match what is returned.");
//   }

//   // Adopting a pet
// function adopt(uint petId) public returns (uint) {
//   require(petId >= 0 && petId <= 15);

//   adopters[petId] = msg.sender;

//   return petId;
// }

//   // Testing retrieval of a single pet's owner
//   function testGetAdopterAddressByPetId() public {
//     address adopter = adoption.adopters(expectedPetId);

//     Assert.equal(adopter, expectedAdopter, "Owner of the expected pet should be this contract");
//   }

//   // Testing retrieval of all pet owners
//   function testGetAdopterAddressByPetIdInArray() public {
//     // Store adopters in memory rather than contract's storage
//     address[16] memory adopters = adoption.getAdopters();

//     Assert.equal(adopters[expectedPetId], expectedAdopter, "Owner of the expected pet should be this contract");
//   }

}