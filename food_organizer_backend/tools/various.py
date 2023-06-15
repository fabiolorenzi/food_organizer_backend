def tokenToDictionary(token):
    tokenDict = {}
    tokenLines = token.split(">>")
    tokenPairs = []
    for couple in tokenLines:
        tokenPairs.append(couple.split(":"))
    for pair in tokenPairs:
        tokenDict[pair[0]] = pair[1]
    return tokenDict
