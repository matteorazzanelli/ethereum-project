
// // Global variables
// const campForm = document.getElementById('newCampaignForm');
// let currentAccount = null;

// const ethereumButton = document.querySelector('.enableEthereumButton');
// const showAccount = document.querySelector('.showAccount');

// ethereumButton.addEventListener('click', () => {
//   getAccount();
// });

// async function getAccount() {
//   const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
//   currentAccount = accounts[0];
//   showAccount.innerHTML = currentAccount;
// }


// // Global variables
// let currentAccount = null;
// const contractAddress = "0x86D219D65452b013912B2af7b2E65E903fa3777d";
// let contract = null;
// let web3 = null;

// const connectButton = document.getElementById('connectButton');
// const contributeSection = document.getElementById('contribute');
// const newCampaignSection = document.getElementById('newCampaign');
// const refs = document.getElementById('refs');
// const contForm = document.getElementById('contributeForm');
// const campForm = document.getElementById('newCampaignForm');



// function handleAccountsChanged(accounts) {
//     if (accounts.length === 0) {
//         console.log('Please connect to MetaMask.');
//         alert('Please connect to MetaMask.');
//     } else if (accounts[0] !== currentAccount) {

//         // Set current account
//         currentAccount = accounts[0];

//         // Change site layout
//         connectButton.removeEventListener('click', login);
//         connectButton.classList.remove('w3-black');
//         connectButton.innerText = 'Connected to MetaMask';
//         connectButton.style.backgroundColor = '#ADFF2F';
//         connectButton.style.cursor = 'default';

//         // Enable interacting with the contract
//         contributeSection.style.display = 'block';
//         newCampaignSection.style.display = 'block';
//         refs.style.display = 'block';
//     }
// }

// // Check for a provider
// async function init() {
//     const provider = await detectEthereumProvider();
//     if (provider) {

//     // Execute app
//     startApp(provider);

//     } else {

//     // Warn
//     console.error('MetaMask is not installed');
//     connectButton.innerText = 'Metamask is not available';
//     connectButton.classList.remove('w3-black');
//     connectButton.style.backgroundColor = "grey";
//     connectButton.style.cursor = "not-allowed";
//     alert('Please install MetaMask to access the page properly');

//     }
// }

// // Permit connection with MetaMask if it is installed
// function startApp(provider) {

//   if (provider !== window.ethereum) {
//     console.error('Do you have multiple wallets installed?');
//     connectButton.innerText = 'Metamask is not available';
//     connectButton.classList.remove('w3-black');
//     connectButton.style.backgroundColor = "grey";
//     connectButton.style.cursor = "not-allowed";
//     alert('Use a single wallet to access the page properly');
//   }
//   else
//   {
//     // Enbale connection
//     connectButton.addEventListener('click', login);
//   }

// }

// // Connect to MetaMask
// async function login() {

//     ethereum
//       .request({ method: 'eth_requestAccounts' })
//       .then(handleAccountsChanged)
//       .catch((err) => {
//         if (err.code === 4001) {
//           // EIP-1193 userRejectedRequest error
//           // If this happens, the user rejected the connection request.
//           console.log('Please connect to MetaMask.');
//         } else {
//           console.error(err);
//         }
//       });

//     try {
//         // Initialize web3
//         web3 = new Web3(window.ethereum);
//         web3.eth.defaultAccount = currentAccount;

//         // Reference to the smart contract
//         contract = new web3.eth.Contract(
//             abi,
//             contractAddress
//         );

//     }
//     catch (error) {
//         console.error(error);
//     }
// }


// // Handle events
// ethereum.on('chainChanged', handleChainChanged);
// ethereum.on('accountsChanged', handleAccountsChanged);
// ethereum.on('connect', (info) => {
//     console.log(`Connected to network ${info}`);
// });

// function handleChainChanged(_chainId) {
//     window.location.reload();
//   }

// // Handle request for contribute contract method
// async function contribute() {
//     const campaignID = contForm.elements['campaignID'].value;
//     const amount = contForm.elements['amount'].value;

//     try {
//     await contract.methods.contribute(campaignID).send({
//         from : currentAccount,
//         value : amount
//     }).then( (result) => {
//         console.log(result);
//         alert('Your contribution was sent correctly. Thank you!');
//     });
//     }
//     catch (error) {
//         console.error(error);
//         alert(error.message);
//     }
// }

// // Handle request for newCampaign contract method
// async function newCampaign()
// {
//     const beneficiary = campForm.elements['beneficiary'].value;
//     const description = campForm.elements['description'].value;
//     const goal = campForm.elements['goal'].value;
//     const deadline = campForm.elements['deadline'].value;

//     try {
//         await contract.methods.newCampaign(beneficiary, description, goal, deadline).send({
//             from : currentAccount
//         }).then( async (result) => {
//             console.log(result);
//             const newID = await contract.methods.numCampaigns().call();
//             alert(`The campaign was successfully created. The new campaign ID is ${newID - 1}. Thank you!`);
//         });
//     }
//     catch (error) {
//             console.error(error);
//             alert(error.message);
//         }
// }

// window.addEventListener('DOMContentLoaded', () => {
//     init();
// });

// /* Event listener */

// // Establish a socket connection
// let url = `ws://${window.location.host}/ws/socket-server/`
// const eventsSocket = new WebSocket(url)

// // Handle JSON data sent
// eventsSocket.onmessage = function(e) {

//     let data = JSON.parse(e.data)
//     console.log('Data:', data)

//     let event = document.getElementById('event')

//     event.insertAdjacentHTML('afterbegin',
//         `
//         <div class="w3-third w3-container w3-margin-bottom">
//             <div class="w3-container w3-white">
//                 <p style="font-weight: bold">${data.eventName}</p>
//                 <p>${JSON.stringify(data.eventArgs, null, 4)}</p>
//             </div>
//         </div>
//         `
//         )

// }

// // Contract abi
// // const abi = [


// function w3_open() {
//     document.getElementById("mySidebar").style.display = "block";
//     document.getElementById("myOverlay").style.display = "block";
// }

// function w3_close() {
//     document.getElementById("mySidebar").style.display = "none";
//     document.getElementById("myOverlay").style.display = "none";
// }
