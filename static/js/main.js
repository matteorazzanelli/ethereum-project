
// Global variables
const sendRequestButton = document.getElementById('sendRequestButton');
let currentAccount = null;

// As soon the page is loaded, try to connect metamask
document.addEventListener('DOMContentLoaded', () => {
  if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
    // Enbale connection
    ethereum.request({ method: 'eth_requestAccounts' }).then(changeAccount)
    .catch((err) => {
      if (err.code === 4001) {
        // EIP-1193 userRejectedRequest error
        // If this happens, the user rejected the connection request.
        console.log('Please connect to MetaMask.');
      } else {
        console.error(err);
      }
    });
    // TODO: catch MetaMask disconnection to reload page
  }
  else {
    console.error('MetaMask is not installed');
    sendRequestButton.innerText = 'Metamask is not available';
    sendRequestButton.disabled = true;
    alert('Please install MetaMask to access the page properly');
  }
}
)

function changeAccount(accounts) {
  if (accounts.length === 0) {
      console.log('Please connect to MetaMask.');
      alert('Please connect to MetaMask.');
      location.reload();
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
// Remove event listener
ethereum.removeListener('accountsChanged', handleAccountsChanged);
