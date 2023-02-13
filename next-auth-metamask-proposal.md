I think one of the killer features of blockchain technology is a the ability to have a decentralized authentication.
Users could easily login to normal web apps in 1 click without needing to use an Oauth2 api that tracks all your account creations. 
Accounts could also be pseudonymous and dropped or picked up whenver the user choses. 

A good tutorial is seen here: https://www.toptal.com/ethereum/one-click-login-flows-a-metamask-tutorial and here https://github.com/amaurym/login-with-metamask-demo

This is an example of a pureTS frontend implementation. 

```ts

  const loginButton = document.getElementById("metamask-button") as HTMLButtonElement

  const getNonce = (key: string) => fetch(`/login?publicAddress=${key}`).then((res) => res.text())

  const verifySignature = (signedNonce: string) => fetch("/verify-signature", {
    method: "Post", body: JSON.stringify({ sig: signedNonce }),
    headers: [['content-type', 'application/json']]
  })

  const loginWithMetamask = async () => {
    const accounts = await eth.request({ method: 'eth_requestAccounts' })
    if (!accounts) {
      throw new Error("could not access accounts")
    }
    const key = accounts[0]
    const nonce = await getNonce(key)

    const signedNonce = await eth.request<string>({
      method: 'personal_sign',
      params: [`0x${Buffer.from(nonce).toString('hex')}`, key]
    })
    if (signedNonce) {
      const message = await verifySignature(signedNonce)
    }


  }
  async function onLoginButtonClick() {
    console.log((await loginWithMetamask()))
  }
  ```
 
 This diagram shows the general Flow: 
 
 
![image](https://user-images.githubusercontent.com/48411623/218500956-f78236ac-b75a-4fa7-8c04-5edad0fbb4f9.png)


Possible Implementation:


![image](https://www.plantuml.com/plantuml/png/RP11IyOm38Rl-nKltrdHSq4T8k8kNcJWjUlY39kjDAawPF_TJDXt6Ekb8UHvyv1Qr6Sj7rFrc5DKYZqkRt7lmxYM3bS3wNEAWUwAK6xwc-kVr_shjd4ZjnI7txXY3gSdHcli1Judya8G7YBqdGKZpT047mA989MCR-g4bT2spOFRhJajHuwc-4MPt-ONY_LQCg5B_MpxPMkOmu7rEVJO_Z-KoKhDXHPucrXF01O8AJZQ9y8fGfFnLMsStV4F)
  
Next-auth could have a Blockchain option in addition to Oauth,Passwordless, and Plain Username-password authentication.
Maybe Metamask could be officially supported, with a custom Blockchain option like the custom Oauth option. 


