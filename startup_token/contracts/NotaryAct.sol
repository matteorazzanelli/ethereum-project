
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Crowdfunding platform
/// @author Matteo Razzanelli
/// @notice This contract was created for educational purpose, its reliability is not guaranteed
/// @dev All functions calls are currently implemented without side effects

import "./parents/ERC20.sol";
import "./parents/SafeMath.sol";
pragma experimental ABIEncoderV2;


/**
 * @title Notary Token contract
 * @dev This is a ERC20 Token.
 * 
 * The token has no initial supply but token are generated when:
 * - contract have been completed;
 * - new user added (to incentivize)
 *
 * The platform owns the contract.
 */
contract NotaryToken is ERC20 {

  // States
  address payable owner_;
  mapping(address => bool) private users_;

  // Events
  event UserAdded(address indexed account);
  event UserRemoved(address indexed account);

  // Constructor
  constructor() ERC20("Notary Token", "NTT") {
    owner_ = payable(msg.sender);
    _mint(msg.sender, 0);
  }

  // Access control modifier
  modifier onlyOwner {
    require(msg.sender == owner_, "Only the contract owner_ can call this function");
    _;
  }

  // Contract destructor
  function destroy() public onlyOwner {
    selfdestruct(owner_);
  } 

  // Add a new client
  function addUser(address user) public onlyOwner {
    users_[user] = true;
    _mint(user, 1); // mint a token when adding user
    emit UserAdded(user);
  }

  // Remove a client
  function removeUser(address user) public onlyOwner {
    users_[user] = false;
    _burn(user, balanceOf(user)); // burn the token previously created
    emit UserRemoved(user);
  }

  // Return if the user is a client or not.
  function isUser(address user) public view returns (bool) {
    return users_[user];
  }

}

/**
* @title Notary platform contract
* @dev This is the implementation of the notary platform associated with the token.
*/
contract NotaryContract is NotaryToken {

  using SafeMath for uint;

  // The platform is idenified by the set of contracts, each contract as a proper structure
  struct TitleDeed {
    address payable buyer;
    address payable seller;
    string description;
    uint amount;
    uint amount_for_now;
    uint deadline;
    bool completed;
  }
  uint public numContract_ = 0;
  uint public constant minPeriodOfDeadline_ = 1 weeks;
  mapping (uint => TitleDeed) public acts_;

  // Events
  event NewContractCreated(uint indexed actID, address indexed buyer, address indexed seller, uint amount);
  event NewContribution(uint indexed actID, address indexed from, uint indexed amount);
  event GoalReached(uint indexed actID, uint indexed timestamp);
  event ActFailed(uint indexed actID, uint indexed timestamp, uint amount);
  event GeneralDeposit(address indexed from, uint amount);

  // Constructor
  constructor () NotaryToken () {}

  // Add a new contract
  function newContract(address payable buyer, address payable seller, string memory description, uint amount, uint deadline) external {
    // Initial check
    require(buyer != address(0), "Zero address entered for the buyer!");
    require(seller != address(0), "Zero address entered for the seller!");
    require(amount > 0, "Amount of the contract has to be a positive value");
    require(deadline > block.timestamp, "Set a future deadline!");
    require(deadline.sub(block.timestamp) > minPeriodOfDeadline_, "Set a greater deadline!");

    NotaryToken.addUser(buyer);
    NotaryToken.addUser(seller);

    uint actID = numContract_++;

    acts_[actID] = TitleDeed (buyer, seller, description, amount, 0, deadline, false);

    emit NewContractCreated(actID, acts_[actID].buyer, acts_[actID].seller, acts_[actID].amount);
  }

  // Contribute in an act of sale
  function newPayment(uint actID) external payable {
    require(acts_[actID].completed == false, "Contract has been already completed!");
    require(acts_[actID].amount > 0, "ActID is not correct!");
    require(acts_[actID].deadline > block.timestamp, "Deadline has already been reached!");
    require(msg.value > 0, "Offer value has to be greater than zero");

    acts_[actID].amount = acts_[actID].amount.add(msg.value);

    emit NewContribution(actID, msg.sender, msg.value);

    // Reward contributor with tokens proportional to contribution
    _mint(msg.sender, msg.value*1/10);

    // Check if contract has been completed
    if(acts_[actID].amount <= acts_[actID].amount_for_now) {
      acts_[actID].completed = true;
      acts_[actID].seller.transfer(acts_[actID].amount_for_now);
      acts_[actID].amount = 0;

      // Reward buyer with further NTT tokens
      ERC20._mint(acts_[actID].buyer, 1000);

      // Notify goal reached
      emit GoalReached(actID, block.timestamp);
    }
  }

  // Check if goal reached
  function checkGoalReached(uint actID) public view returns (bool) {
    return acts_[actID].completed;
  }

  // Refund policy
  function deletedNotaryAct(uint actID) public {
    require(acts_[actID].amount > 0, "ID is not correct!");
    require(block.timestamp > acts_[actID].deadline, "Contract is still in progress!");
    require(acts_[actID].completed == false, "Contract has been successfully completed!");
    require(acts_[actID].buyer == msg.sender, "You have been already refunded or you are not a funder!");

    // For simplicity only the original buyer is refunded
    uint amountFunded = acts_[actID].amount;
    acts_[actID].amount = 0;
    payable(msg.sender).transfer(amountFunded);

    emit ActFailed(actID, block.timestamp, amountFunded);
  }

  function getBuyer(uint actID) external view returns (address payable) {
    return acts_[actID].buyer;
  }

  // We have to create our own getter
  function getTitleDeed(uint actID) public view returns (TitleDeed memory) {
    return acts_[actID];
  }

  // Fallback function: accept any incoming amount
  receive() external payable {
    emit GeneralDeposit(msg.sender, msg.value);
  }
}