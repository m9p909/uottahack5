(() => {
  // scripts/metamask.ts
  var eth = window.ethereum;
  var setupLogin = () => {
    const loginButton = document.getElementById("metamask-button");
    const getNonce = (key) => fetch(`/login?publicAddress=${key}`).then((res) => res.text());
    const verifySignature = (signedNonce, sig) => fetch("/verify-signature", {
      method: "Post",
      body: JSON.stringify({ message: signedNonce, sig }),
      headers: [["content-type", "application/json"]]
    });
    const loginWithMetamask = async () => {
      const accounts = await eth.request({ method: "eth_requestAccounts" });
      if (!accounts) {
        throw new Error("could not access accounts");
      }
      const key = accounts[0];
      const nonce = await getNonce(key);
      const sig = crypto.randomUUID();
      const signedNonce = await eth.request({
        method: "personal_sign",
        params: [nonce, key, sig]
      });
      if (signedNonce) {
        const message = await verifySignature(signedNonce, sig);
      }
    };
    async function onLoginButtonClick() {
      console.log(await loginWithMetamask());
    }
    if (!eth && loginButton) {
      loginButton.innerText = "install Metamask";
      loginButton.disabled = false;
    }
    if (loginButton) {
      loginButton.onclick = onLoginButtonClick;
    } else {
      throw new Error("no login button");
    }
  };
  function main() {
    setupLogin();
  }
  window.onload = main;
})();
