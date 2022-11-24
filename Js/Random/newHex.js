while (true) {
    var hex = prompt('Enter a hex number');
    // Check if the user entered a hex number

    console.log(darken(desaturate(hex, 1.23), 6.86));
}