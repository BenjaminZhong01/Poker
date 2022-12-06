let getLeaderboardUsernameId = (rank) => `username_${rank}`
let getLeaderboardRankNumId = (rank) => `rank_${rank}`
let getLeaderboardImageId = (rank) => `header_${rank}`
let getRoomRowId = (roomNumber) => `room_info_${roomNumber}`
let getCommunityCardId = (cardIndex) => `card${cardIndex}`
let getOptionElementId = (localSeatNumber) => `p${localSeatNumber}_option`
let getBetId = (localSeatNumber) => `p${localSeatNumber}_bet`
let getUserAmountId = (localSeatNumber) => `p${localSeatNumber}_amount`
let getOtherUserCardId = (localSeatNumber, cardIndex) => `p${localSeatNumber}_card${cardIndex}`
let getOtherUserImageId = (localSeatNumber) => `p${localSeatNumber}_image`
let getOtherUserChipId = (localSeatNumber) => `p${localSeatNumber}_chip`
let getOtherUserNameId = (localSeatNumber) => `p${localSeatNumber}_name`
let getOtherUserHandDivId = (localSeatNumber) => `p${localSeatNumber}_hand`
let getDealerElementId = (localSeatNumber) => `D_${localSeatNumber}`

const NUMBER_OF_SEATS_PER_TABLE = 10
const SUIT_TO_CHAR_MAP = {
    "♣": "c",
    "♠": "s",
    "♥": "h",
    "♦": "d"
}
const BUTTON_COLOR_MAP = {
    "button1": "rgba(219.93750303983688, 28.408598005771637, 28.408598005771637, 1)",
    "button2": "rgba(231.62500709295273, 131.25416815280914, 38.60416531562805, 1)",
    "button3": "rgba(33.698962926864624, 183.81250709295273, 57.71714352071285, 1)",
    "button4": "rgba(4.382806420326233, 86.77965223789215, 210.37499696016312, 1)",
    "button5": "rgba(8.44688594341278, 186.22546881437302, 225.24999797344208, 1)",
    "button6": "rgba(235.87500303983688, 216.6118910908699, 43.243746757507324, 1)"

}




const getLeaderboardUserEndpoint = '/texas/leaders'
const mediaFileFolder = '/static/texas'
const joinRoomEndpoint = '/texas/join'
const createRoomEndpoint = '/texas/createRoom'
const exitRoomEndpoint = '/texas/exitRoom'
const roomNumInputId = 'room_number_input'
const gamePageEndpoint = '/game'
const mainPageEndpoint = '/main'
const getRoomGameInfoEndpoint = '/texas/roomGameInfo'
const getAvailableRoomsEndpoint = '/texas/availableRooms'
const availableRoomsListId = 'available_rooms'
const readyEndpoint = '/game/ready'
const cancelReadyEndpoint = '/game/unready'

const cardImagesParentPath = '/static/texas/images/Cards'


var maxRaiseAmount = 0


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

function hideExtraRank(rank) {
    for (let i = rank; i <= 3; i++) {
        imageElement = document.getElementById(getLeaderboardImageId(i))
        usernameElement = document.getElementById(getLeaderboardUsernameId(i))
        rankNumElement = document.getElementById(getLeaderboardRankNumId(i))
        if (imageElement !== null && usernameElement !== null && rankNumElement !== null) {
            imageElement.style.display = "none"
            usernameElement.style.display = "none"
            rankNumElement.style.display = "none"
        }
    }
}

function showRankDiv(rank) {
    imageElement = document.getElementById(getLeaderboardImageId(rank))
    usernameElement = document.getElementById(getLeaderboardUsernameId(rank))
    rankNumElement = document.getElementById(getLeaderboardRankNumId(rank))
    if (imageElement !== null && usernameElement !== null && rankNumElement !== null) {
        imageElement.style.display = "block"
        usernameElement.style.display = "block"
        rankNumElement.style.display = "block"
    }

}


function displayLeaderboardUsers(leaderboardUsers) {
    let rank = 0
    for (let i = 0; i < leaderboardUsers.length; i++) {
        currentUser = leaderboardUsers[i]
        rank = i + 1

        showRankDiv(rank)

        let usernameElement = document.getElementById(getLeaderboardUsernameId(rank))
        if (usernameElement != null) {
            usernameElement.innerText = currentUser['username']
        }
        if (currentUser['picture_url'] !== '') {
            let headerImageElement = document.getElementById(getLeaderboardImageId(rank))
            if (headerImageElement != null) {
                headerImageElement.src = `${currentUser['picture_url']}`
            }
        }
    }

    rank += 1


    hideExtraRank(rank)
}

function updateLeaderboard() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            let leaderboardUsers = JSON.parse(xhr.responseText)

            displayLeaderboardUsers(leaderboardUsers)
        }
    }
    xhr.open('GET', getLeaderboardUserEndpoint)
    xhr.send()

}

function jumpToGamePage() {
    console.log('jumping page')
    let origin = window.location.origin
    let gameUrl = `${origin}${gamePageEndpoint}`
    window.location.assign(gameUrl)
    return false
}

function jumpToMainPage() {
    let origin = window.location.origin
    let mainUrl = `${origin}${mainPageEndpoint}`
    window.location.assign(mainUrl)
    return false
}

function displayRoom(roomGameInfo) {
    console.log('Displaying room.')
    console.log(`Display room with info: ${roomGameInfo}`)
    return
}

function joinRoom() {
    let roomNumInputElement = document.getElementById(roomNumInputId)
    let roomNum = roomNumInputElement.value
    let request_body = {
        'roomNumber': roomNum
    }
    if (roomNum.length > 0) {
        let xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                console.log(xhr.status)
                if (xhr.status == 200) {
                    let roomGameInfo = JSON.parse(xhr.responseText)
                    jumpToGamePage()
                }
            }
        }
        xhr.open('POST', joinRoomEndpoint, true)
        xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
        xhr.send(new URLSearchParams(request_body))
    }
}

function createRoom() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let roomGameInfo = JSON.parse(xhr.responseText)
                jumpToGamePage()
            }
        }
    }
    xhr.open('POST', createRoomEndpoint, true)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.send()
}

function exitRoom() {
    let xhr = new XMLHttpRequest()
    xhr.open('DELETE', exitRoomEndpoint)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.send()
}

function leaveRoom() {
    /* This is used for leave room button */
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                jumpToMainPage()
            }
        }
    }
    xhr.open('DELETE', exitRoomEndpoint)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.send()
}

function displayRoomNumber(roomNumber) {
    let roomNumberElement = document.getElementById("room_number")
    roomNumberElement.innerText = `Room number: ${roomNumber}`
}

function displayRoom(roomInfo) {
    let roomNumber = roomInfo["room_number"]
    displayRoomNumber(roomNumber)
}

function getRoomGameInfoAndDisplay() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            let roomGameInfo = JSON.parse(xhr.responseText)
            let roomInfo = roomGameInfo["room_info"]
            displayRoom(roomInfo)
        }
    }
    xhr.open('GET', getRoomGameInfoEndpoint)
    xhr.send()
}

function createOneAvailableRoomInfo(availableRoomInfo) {
    let oneRow = document.createElement('li')
    let roomNumber = document.createElement('span')
    roomNumber.className = 'room_represent'
    let numberOfPlayers = document.createElement('span')
    numberOfPlayers.className = 'player_number_pre'

    roomNumber.innerText = `Room ${availableRoomInfo['room_number']}`
    numberOfPlayers.innerText = `No. Players: ${availableRoomInfo['number_of_players']}`
    oneRow.appendChild(roomNumber)
    oneRow.appendChild(numberOfPlayers)

    oneRow.id = getRoomRowId(availableRoomInfo['room_number'])

    return oneRow
}

function displayAvailableRooms(availableRoomsInfoList) {
    let availableRoomsElement = document.getElementById(availableRoomsListId)
    removeExtraRoomInfo(availableRoomsInfoList, availableRoomsElement)
    for (let i = 0; i < availableRoomsInfoList.length; i++) {
        let oneRoomInfo = availableRoomsInfoList[i]
        let existingRoomInfoElement = document.getElementById(getRoomRowId(oneRoomInfo['room_number']))
        if (!existingRoomInfoElement) {
            let oneRoomInfoElement = createOneAvailableRoomInfo(oneRoomInfo)
            availableRoomsElement.appendChild(oneRoomInfoElement)
        } else {
            let numberOfPlayersElement = existingRoomInfoElement.getElementsByClassName('player_number_pre')[0]
            numberOfPlayersElement.innerText = `No. Players: ${oneRoomInfo['number_of_players']}`
        }
    }
}

function removeExtraRoomInfo(availableRoomsInfoList, availableRoomsElement) {
    let roomIdSet = new Set()
    for (let i = 0; i < availableRoomsInfoList.length; i++) {
        roomIdSet.add(getRoomRowId(availableRoomsInfoList[i]['room_number']))
    }
    let allRoomsElement = availableRoomsElement.children
    for (let i = 0; i < allRoomsElement.length; i++) {
        let roomElement = allRoomsElement[i]
        if (!roomIdSet.has(roomElement.id)) {
            availableRoomsElement.removeChild(roomElement)
        }
    }
}


function getAvailableRoomsInfo() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            let availableRoomsInfo = JSON.parse(xhr.responseText)
            let availableRoomsInfoList = availableRoomsInfo['available_rooms']
            displayAvailableRooms(availableRoomsInfoList)
        }
    }
    xhr.open('GET', getAvailableRoomsEndpoint)
    xhr.send()
}

function userReady() {
    let userStatus = document.getElementById("ready_button")
    let roomNumber = document.getElementById("room_number")
    let xhr = new XMLHttpRequest()
    if (userStatus.innerText == "Ready") {
        xhr.open('POST', readyEndpoint)
        userStatus.innerText = "Cancel Ready"
    } else {
        xhr.open('POST', cancelReadyEndpoint)
        userStatus.innerText = "Ready"
    }
    let request_body = {
        'roomNumber': roomNumber.innerText
    }
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));
}

//'choice' : "call"/"check"/"fold"/"allin"/"raise+int"
function userFold() {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', gamePageEndpoint)
    let request_body = {
        'choice': "fold"
    }
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));

    // hideGameActionButtons()
}

function userCall() {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', gamePageEndpoint)
    let request_body = {
        'choice': "call"
    }
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));
}

function userRaise() {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', gamePageEndpoint)
    let raiseAmountElement = document.getElementById("raise_amount")
    // let currentRaiseAmount = Number(raiseAmountElement.innerText)
    let currentRaiseAmount = raiseAmountElement.innerText

    console.log("printing amount",currentRaiseAmount)

    let request_body = {
        'choice': "raise"+currentRaiseAmount
    }
    console.log("request_body",request_body)

    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));
}

function userAdd() {
    let raiseAmountElement = document.getElementById("raise_amount")
    let currentRaiseAmount = Number(raiseAmountElement.innerText)

    if (currentRaiseAmount+5<=maxRaiseAmount){
        raiseAmountElement.innerText=(currentRaiseAmount+5).toString()
    }else {
        raiseAmountElement.innerText=maxRaiseAmount.toString()
    }

}

function userMinus() {
    let raiseAmountElement = document.getElementById("raise_amount")
    let currentRaiseAmount = Number(raiseAmountElement.innerText)

    if (currentRaiseAmount-5>=0){
        raiseAmountElement.innerText=(currentRaiseAmount-5).toString()
    }else {
        raiseAmountElement.innerText="0"
    }

}


function userAllIn() {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', gamePageEndpoint)

    let request_body = {
        'choice': "raise"+maxRaiseAmount.toString()
    }
    console.log("request_body",request_body)

    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));

}


// Sends a new request to update the game
function updateGame() {

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
    }
    let roomNumber = document.getElementById("room_number")
    let request_body = {
        'roomNumber': roomNumber.innerText
    }
    xhr.open("POST", gamePageEndpoint, true)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(new URLSearchParams(request_body));
}

function updatePage(xhr) {
    // console.log(xhr.status)
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateStatus(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    // let errorElement = document.getElementById("error")
    // errorElement.innerHTML = message
}

function displayOneElement(elementId, displayStyle) {
    let element = document.getElementById(elementId)
    if (element !== null) {
        element.style.display = displayStyle
    }
}

function hideOneElement(elementId) {
    let element = document.getElementById(elementId)
    if (element !== null) {
        element.style.display = "none"
    }
}

function enableRaiseButton(raiseAmountElement, raise, plus, minus) {
    let currentRaiseAmount = Number(raiseAmountElement.innerText)
    raise.style.display = "inline"
    enableButton(raise)
    if (currentRaiseAmount < maxRaiseAmount) {
        enableButton(plus)
    } else {
        raiseAmountElement.innerText = maxRaiseAmount.toString()
        disableButton(plus)
    }

    if (currentRaiseAmount > 0) {
        enableButton(minus)
    } else {
        raiseAmountElement.innerText = "0"
        disableButton(minus)
    }
}

function disableButton(buttonElement) {
    buttonElement.disabled = true
    buttonElement.style.backgroundColor = "gray"
}

function enableButton(buttonElement) {
    buttonElement.disabled = false
    buttonElement.style.backgroundColor = BUTTON_COLOR_MAP[buttonElement.id]
}


function displayGameActionButtons(is_your_turn, buttonCase){
    let fold = document.getElementById("button1")
    let callCheck = document.getElementById("button2")
    let raise = document.getElementById("button3")
    let allin = document.getElementById("button4")
    let plus = document.getElementById("button5")
    let minus = document.getElementById("button6")

    let raiseAmountElement = document.getElementById("raise_amount")

    //TODO: remove hardcode here:
    // 0: no buttons available, 1: only raise to 5 available, 2: only raise to 10 available, 3: call+raise+fold, 4: check+raise, 5: allin, 6: folded
    // buttonCase=4

    console.log(buttonCase)
    console.log(is_your_turn)
    fold.style.display = "inline"
    callCheck.style.display = "inline"
    raise.style.display = "inline"
    allin.style.display = "inline"
    plus.style.display = "inline"
    minus.style.display = "inline"
    if (is_your_turn){

        if (buttonCase == 0) {
            disableButton(fold)
            disableButton(callCheck)
            disableButton(raise)
            disableButton(allin)
            disableButton(plus)
            disableButton(minus)
        } else if (buttonCase == 1) {
            disableButton(fold)
            disableButton(callCheck)

            if (5 > maxRaiseAmount) {
                raiseAmountElement.innerText = maxRaiseAmount.toString()
            } else {
                raiseAmountElement.innerText = "5"
            }
            enableButton(raise)

            disableButton(allin)
            disableButton(plus)
            disableButton(minus)
        } else if (buttonCase == 2) {
            disableButton(fold)
            disableButton(callCheck)


            if (10 > maxRaiseAmount) {
                raiseAmountElement.innerText = maxRaiseAmount.toString()
            } else {
                raiseAmountElement.innerText = "5"
            }
            enableButton(raise)

            disableButton(allin)
            disableButton(plus)
            disableButton(minus)
        } else if (buttonCase == 3) {
            enableButton(fold)

            callCheck.innerText = "Call"
            enableButton(callCheck)

            enableRaiseButton(raiseAmountElement, raise, plus, minus)

            enableButton(allin)
            enableButton(fold)
            disableButton(allin)

        } else if (buttonCase == 4) {

            disableButton(fold)

            callCheck.innerText = "Check"
            enableButton(callCheck)
            enableRaiseButton(raiseAmountElement, raise, plus, minus)
            enableButton(allin)
        } else if (buttonCase == 5) {
            disableButton(fold)
            disableButton(callCheck)
            disableButton(raise)
            enableButton(allin)
            disableButton(plus)
            disableButton(minus)
        } else if (buttonCase == 6) {
            enableButton(fold)

            disableButton(callCheck)
            disableButton(raise)
            disableButton(allin)
            disableButton(plus)
            disableButton(minus)
        } else {
            enableButton(fold)
            enableButton(callCheck)
            enableButton(raise)
            enableButton(allin)
            enableButton(plus)
            enableButton(minus)
        }
    } else {

        // fold.style.display = "none"
        // callCheck.style.display = "none"
        // raise.style.display = "none"
        // allin.style.display = "none"
        // plus.style.display = "none"
        // minus.style.display = "none"
        disableButton(fold)
        disableButton(callCheck)
        disableButton(raise)
        disableButton(allin)
        disableButton(plus)
        disableButton(minus)

    }
}

function disableAllButtons() {
    let fold = document.getElementById("button1")
    let callCheck = document.getElementById("button2")
    let raise = document.getElementById("button3")
    let allin = document.getElementById("button4")
    let plus = document.getElementById("button5")
    let minus = document.getElementById("button6")

    disableButton(fold)
    disableButton(callCheck)
    disableButton(raise)
    disableButton(allin)
    disableButton(plus)
    disableButton(minus)
}

function hideGameActionButtons() {
    let button1 = document.getElementById("button1")
    let button2 = document.getElementById("button2")
    let button3 = document.getElementById("button3")
    let button4 = document.getElementById("button4")
    let button5 = document.getElementById("button5")
    let button6 = document.getElementById("button6")
    button1.style.display = "none"
    button2.style.display = "none"
    button3.style.display = "none"
    button4.style.display = "none"
    button5.style.display = "none"
    button6.style.display = "none"
}

function displayRoomActionButtons() {
    let leaveRoom = document.getElementById("leave_button")
    let readyButton = document.getElementById("ready_button")
    leaveRoom.style.display = "inline"
    readyButton.style.display = "inline"
}

function hideRoomActionButtons() {
    let leaveRoom = document.getElementById("leave_button")
    let readyButton = document.getElementById("ready_button")
    leaveRoom.style.display = "none"
    readyButton.style.display = "none"
}

function displayPotAmount(potAmount) {
    let potAmountElement = document.getElementById("pot")
    potAmountElement.innerText = potAmount
}

function getCardImagePath(cardStr) {
    let suit = SUIT_TO_CHAR_MAP[cardStr.charAt(cardStr.length - 1)]
    let valueStr = cardStr.substring(0, cardStr.length - 1)
    let cardName = valueStr.concat(suit)
    return `${cardImagesParentPath}/${cardName}.png`
}

function displayCommunityCards(communityCardsList, round) {
    if (communityCardsList.length == 0) {
        hideCommunityCards()
        return
    }
    let displayCardsList = []
    if (round == 1) {
        displayCardsList = communityCardsList.slice(0, 3)
    } else if (round == 2) {
        displayCardsList = communityCardsList.slice(0, 4)
    } else if (round == 3) {
        displayCardsList = communityCardsList
    } else if (round == 0) {
        hideCommunityCards()
        return
    }

    for (let i = 0; i < displayCardsList.length; i++) {
        let cardIndex = i + 1  // Do notice that in game.html, community cards index start at 1.
        let cardElement = document.getElementById(getCommunityCardId(cardIndex))
        let cardStr = displayCardsList[i]
        cardElement.style.backgroundImage = `url(${getCardImagePath(cardStr)})`
    }
}

function hideCommunityCards() {
    for (let i = 1; i < 6; i++) {
        let cardElement = document.getElementById(getCommunityCardId(i))
        cardElement.style.backgroundImage = ''
    }
}

function getLocalSeatNumber(userSeatNumber, selfSeatNumber) {
    // This function is used to obtain the seat of the other users on current page. 
    // We do this because for each user the table looks different.
    let localSeatNumber = userSeatNumber - selfSeatNumber
    if (localSeatNumber < 0) {
        localSeatNumber += NUMBER_OF_SEATS_PER_TABLE
    }
    return localSeatNumber
}

function getSelfSeatNumber(response) {
    for (let i = 1; i < response.length; i++) {
        let userInfo = response[i]
        if (userInfo["user"] == selfUserId) {
            return userInfo["seat_number"]
        }
    }

    return 0
}

function displayOption(userInfo, localSeatNumber) {
    let otherUserOptionElement = document.getElementById(getOptionElementId(localSeatNumber))
    if (userInfo["last_choice"].length > 0) {
        otherUserOptionElement.innerText = userInfo["last_choice"]
        switch (userInfo["last_choice"]) {
            case "Not":
                otherUserOptionElement.style.backgroundColor = BUTTON_COLOR_MAP["button5"]
                break
            case "Ready":
                otherUserOptionElement.style.backgroundColor = BUTTON_COLOR_MAP["button4"]
                break
            case "Fold":
                otherUserOptionElement.style.backgroundColor = BUTTON_COLOR_MAP["button1"]
                break
            case "Call":
                otherUserOptionElement.style.backgroundColor = BUTTON_COLOR_MAP["button2"]
                break
            case "Raise":
                otherUserOptionElement.style.backgroundColor = BUTTON_COLOR_MAP["button3"]
                break
        }
    } else {
        if (userInfo["ready"] == "not") {
            otherUserOptionElement.innerText = "Not"
        } else {
            otherUserOptionElement.innerText = "Ready"
        }
    }
}

function displayBet(betAmount, localSeatNumber) {
    let betElement = document.getElementById(getBetId(localSeatNumber))
    betElement.innerText = betAmount
}

function displayAmount(chipsAmount, localSeatNumber) {
    let amountElement = document.getElementById(getUserAmountId(localSeatNumber))
    amountElement.innerText = chipsAmount
}

function displayUsername(username, localSeatNumber) {
    let usernameElement = document.getElementById(getOtherUserNameId(localSeatNumber))
    usernameElement.innerText = username
}

function displayOneOtherUser(userInfo, selfSeatNumber, gameInfo, pos, p1) {
    if (p1.length == 0) {
        localSeatNumber = getLocalSeatNumber(userInfo["seat_number"], selfSeatNumber)
        // console.log("localSeatNumber",localSeatNumber)
    } else if (pos == -1) {
        localSeatNumber = p1.pop()
    } else {
        localSeatNumber = p1[pos]
    }
    displayOption(userInfo, localSeatNumber)
    displayBet(userInfo["bet"], localSeatNumber)
    displayAmount(userInfo["chips"], localSeatNumber)
    displayUsername(`${userInfo["firstname"]} ${userInfo["lastname"]}`, localSeatNumber)
    if (gameInfo["won"] && !userInfo['folded'] && gameInfo['displaycard']) {
        displayOneOtherUserHands(userInfo["cards_holding"], localSeatNumber)
    }
    displayDealer(userInfo, gameInfo, localSeatNumber)
}

function displayDealer(userInfo, gameInfo, localSeatNumber) {
    // console.log(getDealerElementId(localSeatNumber))
    let dealerElement = document.getElementById(getDealerElementId(localSeatNumber))
    if (gameInfo["status"] == "start" && gameInfo["dealer_id"] && gameInfo["dealer_id"] == userInfo["user"]) {
        dealerElement.style.display = "inline"
    } else {
        dealerElement.style.display = "none"
    }
}

function displaySelf(userInfo, gameInfo) {
    let selfAmountElement = document.getElementById("my_amount")
    selfAmountElement.innerText = userInfo["chips"]

    let selfBetElement = document.getElementById("my_bet")
    selfBetElement.innerText = userInfo["bet"]
    displayMyCard(userInfo['cards_holding'])
    displayDealer(userInfo, gameInfo, 0)

    // console.log("gameInfo.status",gameInfo.status,(gameInfo.status=="start"))

    if (gameInfo.status=="start"){
        let is_your_turn = (gameInfo.player_to_bet_id == selfUserId)
        console.log("is_your_turn",is_your_turn)

        displayGameActionButtons(is_your_turn, userInfo["buttons"])
    }

}

function displayMyCard(myCardList) {
    if (myCardList.length) {
        let myCard1 = document.getElementById("mycard1")
        let myCard2 = document.getElementById("mycard2")
        let cardStr1 = myCardList[0]
        let cardStr2 = myCardList[1]

        myCard1.style.backgroundImage = `url(${getCardImagePath(cardStr1)})`
        myCard2.style.backgroundImage = `url(${getCardImagePath(cardStr2)})`
        myCard1.style.display = 'inline'
        myCard2.style.display = 'inline'
    }
}

function hideMyCard() {
    let myCard1 = document.getElementById("mycard1")
    let myCard2 = document.getElementById("mycard2")

    myCard1.style.display = 'none'
    myCard2.style.display = 'none'

}

function displayOneOtherUserHands(otherUserCardsList, localSeatNumber) {
    let handDivElement = document.getElementById(getOtherUserHandDivId(localSeatNumber))
    let cardElement1 = document.getElementById(getOtherUserCardId(localSeatNumber, 1))
    let cardElement2 = document.getElementById(getOtherUserCardId(localSeatNumber, 2))

    let cardStr1 = otherUserCardsList[0]
    let cardStr2 = otherUserCardsList[1]

    handDivElement.style.display = 'flex'
    cardElement1.style.backgroundImage = `url(${getCardImagePath(cardStr1)})`
    cardElement2.style.backgroundImage = `url(${getCardImagePath(cardStr2)})`
}

function hideOtherUserHands() {
    for (let i = 1; i < 10; i++) {
        let handDivElement = document.getElementById(getOtherUserHandDivId(i))
        let cardElement1 = document.getElementById(getOtherUserCardId(i, 1))
        let cardElement2 = document.getElementById(getOtherUserCardId(i, 2))

        handDivElement.style.display = 'none'
        cardElement1.style.backgroundImage = ''
        cardElement2.style.backgroundIMage = ''
    }
}

function hideOneUser(localSeatNumber) {
    // Hide/Show hand is handled differently.
    let userImage = document.getElementById(getOtherUserImageId(localSeatNumber))
    let userOption = document.getElementById(getOptionElementId(localSeatNumber))
    let userAmount = document.getElementById(getUserAmountId(localSeatNumber))
    let userChips = document.getElementById(getOtherUserChipId(localSeatNumber))
    let userBet = document.getElementById(getBetId(localSeatNumber))
    let username = document.getElementById(getOtherUserNameId(localSeatNumber))

    userImage.style.display = 'none'
    userOption.style.display = 'none'
    userAmount.style.display = 'none'
    userChips.style.display = 'none'
    userBet.style.display = 'none'
    username.style.display = 'none'

}

function showOneUser(localSeatNumber) {
    // Hide/Show hand is handled differently
    let userImage = document.getElementById(getOtherUserImageId(localSeatNumber))
    let userOption = document.getElementById(getOptionElementId(localSeatNumber))
    let userAmount = document.getElementById(getUserAmountId(localSeatNumber))
    let userChips = document.getElementById(getOtherUserChipId(localSeatNumber))
    let userBet = document.getElementById(getBetId(localSeatNumber))
    let username = document.getElementById(getOtherUserNameId(localSeatNumber))

    userImage.style.display = 'inline'
    userOption.style.display = 'inline'
    userAmount.style.display = 'inline'
    userChips.style.display = 'inline'
    userBet.style.display = 'inline'
    username.style.display = 'inline'
}

function getTakenSeats(response, selfSeatNumber) {
    let seatNumSet = new Set()
    for (let i = 1; i < response.length; i++) {
        let userInfo = response[i]
        let localSeatNum = getLocalSeatNumber(userInfo['seat_number'], selfSeatNumber)
        seatNumSet.add(localSeatNum)
    }
    return seatNumSet
}

function getWinnerInfo(response, winnerId) {
    for (let i = 1; i < response.length; i++) {
        let userInfo = response[i]
        if (userInfo["user"] == winnerId) {
            return userInfo
        }
    }
    return {}
}

function displayWinner(winnerInfo, selfSeatNumber, gameInfo) {
    let winnerElement = document.getElementById('winner_display')
    winnerElement.style.display = "inline"
    winnerElement.innerText = `WINNER: ${winnerInfo["firstname"]} ${winnerInfo["lastname"]}`
    disableAllButtons()
}


function updateStatus(response) {
    let gameInfo = response[0]

    let selfSeatNumber = getSelfSeatNumber(response)
    let takenSeatSet = getTakenSeats(response, selfSeatNumber)

    if (gameInfo.status == "start") {
        hideRoomActionButtons()
        displayPotAmount(gameInfo['pot'])
        displayCommunityCards(gameInfo['community_cards'], gameInfo["round"])
    } else if (gameInfo.status == "unready") {
        displayRoomActionButtons()
        hideGameActionButtons()
        displayPotAmount("0")
        hideOtherUserHands()
        hideMyCard()
    }

    // console.log("switch case", takenSeatSet.size)
    switch (takenSeatSet.size) {
        case 2:
            projection = [5]
            break
        case 3:
            projection = [6,4]
            break
        case 4:
            projection = [8,5,2]
            break
        case 5:
            projection = [8,6,4,2]
            break
        case 6:
            projection = [8,6,5,4,2]
            break
        case 7:
            projection = [8,7,6,4,3,2]
            break
        case 8:
            projection = [8,7,6,5,4,3,2]
            break
        case 9:
            projection = [9,8,7,6,4,3,2,1]
            break
        default:
            projection = []
    }
    let p1 = projection.slice()
    let selfpos = 0
    for (let i = 1; i < response.length; i++) {
        let userInfo = response[i]
        if (userInfo["user"] == selfUserId) {
            selfpos = i - 1
        }
    }
    // console.log("selfpos", selfpos)
    console.log(response)
    for (let i = 1; i < response.length; i++) {
        let userInfo = response[i]
        if (userInfo["user"] != selfUserId) {
            if (selfpos - i >= 0){
                displayOneOtherUser(userInfo, selfSeatNumber, gameInfo, selfpos - i, p1)
            } else {
                displayOneOtherUser(userInfo, selfSeatNumber, gameInfo, -1, p1)
            }
        } else {
            // displayGameActionButtons(userInfo["buttons"])
            // console.log(userInfo["chips"])
            if (Number.isInteger(gameInfo["highest_bet"]) && Number.isInteger(userInfo["bet"]) && Number.isInteger(userInfo["chips"])) {
                maxRaiseAmount = -gameInfo["highest_bet"] + userInfo["bet"] + userInfo["chips"]
                // maxRaiseAmount = 4
            }
            // console.log(`maxRaiseAmount: ${maxRaiseAmount}`)
            displaySelf(userInfo, gameInfo)
        }
    }
    if (projection.length == 0) {
        for (let i = 1; i < 10; i++) {
            if (!takenSeatSet.has(i)) {
                hideOneUser(i)
            } else {
                showOneUser(i)
            }
        }
    } else {
        for (let i = 1; i < 10; i++) {
            if (!projection.includes(i)) {
                hideOneUser(i)
            } else {
                showOneUser(i)
            }
        }
    }

    if (gameInfo["won"]) {
        let winnerId = gameInfo["winner_id"]
        if (winnerId !== null) {
            let winnerInfo = getWinnerInfo(response, winnerId)
            displayWinner(winnerInfo, selfSeatNumber, gameInfo)
            let userStatus = document.getElementById("ready_button")
            userStatus.innerText = "Ready"
        }
    } else {
        let winnerElement = document.getElementById('winner_display')
        winnerElement.style.display = "none"
    }
}