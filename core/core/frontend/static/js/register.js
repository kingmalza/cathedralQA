

var ccErrorNo = 0;
var ccErrors = new Array ()

ccErrors [0] = "Unknown card type";
ccErrors [1] = "No card number provided";
ccErrors [2] = "Credit card number is in invalid format";
ccErrors [3] = "Credit card number is invalid";
ccErrors [4] = "Credit card number has an inappropriate number of digits";
ccErrors [5] = "Warning! This credit card number is associated with a scam attempt";

var domains = [
  /* Default domains included */
  "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
  "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
  "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",

  /* Other global domains */
  "email.com", "fastmail.fm", "games.com" /* AOL */, "gmx.net", "hush.com", "hushmail.com", "icloud.com",
  "iname.com", "inbox.com", "lavabit.com", "love.com" /* AOL */, "outlook.com", "pobox.com", "protonmail.com",
  "rocketmail.com" /* Yahoo */, "safe-mail.net", "wow.com" /* AOL */, "ygm.com" /* AOL */,
  "ymail.com" /* Yahoo */, "zoho.com", "yandex.com",

  /* United States ISP domains */
  "bellsouth.net", "charter.net", "cox.net", "earthlink.net", "juno.com",

  /* British ISP domains */
  "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",
  "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",
  "virgin.net", "wanadoo.co.uk", "bt.com",

  /* Domains used in Asia */
  "sina.com", "sina.cn", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph", "163.com", "126.com", "aliyun.com", "foxmail.com",

  /* French ISP domains */
  "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr",

  /* German ISP domains */
  "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de" /* T-Mobile */, "web.de", "yahoo.de",

  /* Italian ISP domains */
  "libero.it", "virgilio.it", "hotmail.it", "aol.it", "tiscali.it", "alice.it", "live.it", "yahoo.it", "email.it", "tin.it", "poste.it", "teletu.it",

  /* Russian ISP domains */
  "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru",

  /* Belgian ISP domains */
  "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be",

  /* Argentinian ISP domains */
  "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",

  /* Domains used in Mexico */
  "yahoo.com.mx", "live.com.mx", "hotmail.es", "hotmail.com.mx", "prodigy.net.mx",

  /* Domains used in Brazil */
  "yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br", "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br"
];

function checkEmail(evalue) {
    var ext_domain = evalue.replace(/.*@/, "");
    if (domains.includes(ext_domain.toLowerCase())) {
        alert("Please use a business email address for register your corporate Aida account.");
        document.getElementById('c_email').value = '';
        document.getElementById("c_email").focus();
    }

}

function testCreditCard() {
  myCardNo = document.getElementById('gatewayCardNumber').value;
  myCardType = document.getElementById('ccType').value;
  if (checkCreditCard(myCardNo, myCardType)) {
    //alert("Credit card has a valid format")
  } else {
    alert(ccErrors[ccErrorNo])
      document.getElementById('gatewayCardNumber').value = '';
        document.getElementById("gatewayCardNumber").focus();
  };
}


function checkCreditCard (cardnumber, cardname) {

  // Array to hold the permitted card characteristics
  var cards = new Array();

  // Define the cards we support. You may add addtional card types as follows.

  //  Name:         As in the selection box of the form - must be same as user's
  //  Length:       List of possible valid lengths of the card number for the card
  //  prefixes:     List of possible prefixes for the card
  //  checkdigit:   Boolean to say whether there is a check digit

  cards [0] = {name: "Visa",
               length: "13,16",
               prefixes: "4",
               checkdigit: true};
  cards [1] = {name: "MasterCard",
               length: "16",
               prefixes: "51,52,53,54,55",
               checkdigit: true};
  cards [2] = {name: "DinersClub",
               length: "14,16",
               prefixes: "36,38,54,55",
               checkdigit: true};
  cards [3] = {name: "CarteBlanche",
               length: "14",
               prefixes: "300,301,302,303,304,305",
               checkdigit: true};
  cards [4] = {name: "AmEx",
               length: "15",
               prefixes: "34,37",
               checkdigit: true};
  cards [5] = {name: "Discover",
               length: "16",
               prefixes: "6011,622,64,65",
               checkdigit: true};
  cards [6] = {name: "JCB",
               length: "16",
               prefixes: "35",
               checkdigit: true};
  cards [7] = {name: "enRoute",
               length: "15",
               prefixes: "2014,2149",
               checkdigit: true};
  cards [8] = {name: "Solo",
               length: "16,18,19",
               prefixes: "6334,6767",
               checkdigit: true};
  cards [9] = {name: "Switch",
               length: "16,18,19",
               prefixes: "4903,4905,4911,4936,564182,633110,6333,6759",
               checkdigit: true};
  cards [10] = {name: "Maestro",
               length: "12,13,14,15,16,18,19",
               prefixes: "5018,5020,5038,6304,6759,6761,6762,6763",
               checkdigit: true};
  cards [11] = {name: "VisaElectron",
               length: "16",
               prefixes: "4026,417500,4508,4844,4913,4917",
               checkdigit: true};
  cards [12] = {name: "LaserCard",
               length: "16,17,18,19",
               prefixes: "6304,6706,6771,6709",
               checkdigit: true};

  // Establish card type
  var cardType = -1;
  for (var i=0; i<cards.length; i++) {

    // See if it is this card (ignoring the case of the string)
    if (cardname.toLowerCase () == cards[i].name.toLowerCase()) {
      cardType = i;
      break;
    }
  }

  // If card type not found, report an error
  if (cardType == -1) {
     ccErrorNo = 0;
     return false;
  }

  // Ensure that the user has provided a credit card number
  if (cardnumber.length == 0)  {
     ccErrorNo = 1;
     return false;
  }

  // Now remove any spaces from the credit card number
  cardnumber = cardnumber.replace (/\s/g, "");

  // Check that the number is numeric
  var cardNo = cardnumber
  var cardexp = /^[0-9]{13,19}$/;
  if (!cardexp.exec(cardNo))  {
     ccErrorNo = 2;
     return false;
  }

  // Now check the modulus 10 check digit - if required
  if (cards[cardType].checkdigit) {
    var checksum = 0;                                  // running checksum total
    var mychar = "";                                   // next char to process
    var j = 1;                                         // takes value of 1 or 2

    // Process each digit one by one starting at the right
    var calc;
    for (i = cardNo.length - 1; i >= 0; i--) {

      // Extract the next digit and multiply by 1 or 2 on alternative digits.
      calc = Number(cardNo.charAt(i)) * j;

      // If the result is in two digits add 1 to the checksum total
      if (calc > 9) {
        checksum = checksum + 1;
        calc = calc - 10;
      }

      // Add the units element to the checksum total
      checksum = checksum + calc;

      // Switch the value of j
      if (j ==1) {j = 2} else {j = 1};
    }

    // All done - if checksum is divisible by 10, it is a valid modulus 10.
    // If not, report an error.
    if (checksum % 10 != 0)  {
     ccErrorNo = 3;
     return false;
    }
  }

  // Check it's not a spam number
  if (cardNo == '5490997771092064') {
    ccErrorNo = 5;
    return false;
  }

  // The following are the card-specific checks we undertake.
  var LengthValid = false;
  var PrefixValid = false;
  var undefined;

  // We use these for holding the valid lengths and prefixes of a card type
  var prefix = new Array ();
  var lengths = new Array ();

  // Load an array with the valid prefixes for this card
  prefix = cards[cardType].prefixes.split(",");

  // Now see if any of them match what we have in the card number
  for (i=0; i<prefix.length; i++) {
    var exp = new RegExp ("^" + prefix[i]);
    if (exp.test (cardNo)) PrefixValid = true;
  }

  // If it isn't a valid prefix there's no point at looking at the length
  if (!PrefixValid) {
     ccErrorNo = 3;
     return false;
  }

  // See if the length is valid for this card
  lengths = cards[cardType].length.split(",");
  for (j=0; j<lengths.length; j++) {
    if (cardNo.length == lengths[j]) LengthValid = true;
  }

  // See if all is OK by seeing if the length was valid. We only check the length if all else was
  // hunky dory.
  if (!LengthValid) {
     ccErrorNo = 4;
     return false;
  };

  // The credit card is in the required format.
  return true;
}



function isempty() {
    var r_1;
    var r_2;
    var r_3;
    var r_4;
    var r_5;
    var r_6;
    var r_7;
    var r_8;
    var r_9;
    var r_10;
    var r_11;
    var r_12;
    var r_13;
    var r_14;

    r_1 = document.getElementById("firstname").value;
    r_2 = document.getElementById("lastname").value;
    r_3 = document.getElementById("organisationname").value;
    r_4 = document.getElementById("address1").value;
    r_5 = document.getElementById("city").value;
    r_6 = document.getElementById("state").value;
    r_7 = document.getElementById("country").value;
    r_8 = document.getElementById("taxid").value;
    r_9 = document.getElementById("ccName").value;
    r_10 = document.getElementById("gatewayCardNumber").value;
    r_11 = document.getElementById("gatewayCardExpiryDateMonth").value;
    r_12 = document.getElementById("plan_type").value;
    r_13 = document.getElementById("ccType").value;
    r_14 = document.getElementById("cardCVC").value;
    
    if (r_1 == "") {
        alert("Enter a Valid Firstname");
        return false;
    };
    if (r_2 == "") {
        alert("Enter a Valid Lastname");
        return false;
    };
    if (r_3 == "") {
        alert("Enter a company name");
        return false;
    };
    if (r_4 == "") {
        alert("Enter a Valid Address");
        return false;
    };    
    if (r_12 == "") {
        alert("Select an Economic Plan");
        return false;
    };
    if (r_5 == "") {
        alert("Enter a Valid City");
        return false;
    };
    if (r_6 == "") {
        alert("Enter a Valid State");
        return false;
    };
    if (r_7 == "") {
        alert("Enter a Valid Country");
        return false;
    };
    if (r_8 == "") {
        alert("Enter a Valid Tax ID");
        return false;
    };
    if (r_9 == "") {
        alert("Enter a Valid CreditCard Name");
        return false;
    };
    if (r_10 == "") {
        alert("Enter a CreditCard Number");
        return false;
    };
    if (r_11 == "") {
        alert("Enter a Expyry Date");
        return false;
    };
    if (r_13 == "") {
        alert("Enter a Credit Card type");
        return false;
    };
    if (r_14 == "") {
        alert("Enter the Credit Card CVC");
        return false;
    };
}