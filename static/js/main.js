
// Global variables
const sendRequestButton = document.getElementById('sendRequestButton');
let currentAccount = null;

// As soon the page is loaded, try to connect metamask
window.addEventListener('DOMContentLoaded', () => {
  if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
    // Enbale connection
    ethereum.request({ method: 'eth_requestAccounts' }).then(changeAccount);
    if(currentAccount === null){
      sendRequestButton.disabled = true;
      alert('Waiting...');
    }
    // TODO: catch MetaMask disconnection to reload page
  }
  else {
    console.error('MetaMask is not installed');
    sendRequestButton.innerText = 'Metamask is not available';
    sendRequestButton.classList.remove('w3-black');
    sendRequestButton.style.backgroundColor = "grey";
    sendRequestButton.style.cursor = "not-allowed";
    alert('Please install MetaMask to access the page properly');
  }

});

function changeAccount(accounts) {
  if (accounts.length === 0) {
      console.log('Please connect to MetaMask.');
      alert('Please connect to MetaMask.');
  } else {
    // Set current account
    currentAccount = accounts[0];
    console.log(currentAccount);
    sendRequestButton.disabled = false;
    // write on json
    // const dict_values = {currentAccount};
    // const s = JSON.stringify(dict_values);
    // console.log(s);
    // window.alert(s);
    // $.ajax({
    //   url:"/test",
    //   type:"POST",
    //   contentType: "application/json",
    //   data: JSON.stringify(s)
    // });
  }
}
