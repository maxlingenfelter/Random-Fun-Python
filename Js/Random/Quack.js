const baseXpForLevelOne = 30;
const xpMultiplier = 1.2;

function calcUserLevelFromXp(xp) {
    //This funtion will take in any value for xp and using the baseXpForLevelOne and xpMultiplier will return the level
    //This is a simple function that will be used to determine the level of a player based on their xp
    return Math.floor(Math.log(xp / baseXpForLevelOne) / Math.log(xpMultiplier)) + 1;
}
