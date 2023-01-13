import React, { useState } from 'react';
import { StyleSheet, Button, Text, View } from 'react-native';
// import { Audio } from 'expo-av';

export default function LibrarySongs({ navigation }) {

    // const sound = new Audio.Sound();

    // async function playSound() {
    //     try {
    //         await sound.loadAsync(require('../../assets/audio/Rammstein_-_Adieu.mp3'), { shouldPlay: true });
    //         await sound.replayAsync();
    //         console.log('playing...')
    //         await sound.unloadAsync();
    //     } catch (error) {
    //         console.log(error)
    //     }
    // }

    // async function stopSound() {

    // }

    return (
        <View style={styles.container}>
            <Text style={styles.text}>Songs</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        width: '100%',
        height: '100%',
        flex: 1,
        backgroundColor: 'black',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    }
})