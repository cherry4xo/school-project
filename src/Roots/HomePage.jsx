import React, { useEffect, useState } from "react";
import { Image, ImageBackground, View, Text, StyleSheet } from "react-native";

const bgImage = require('../../assets/img/HomeBG.png')
const avatar = require('../../assets/img/avatar.jpg')

export default function HomePage({ navigation }) {

    const [time, setTime] = useState('')

    useEffect(() => {
        currentTime = new Date().getHours()

        if (currentTime >= 0 && currentTime < 6) {
            setTime('night')
        }
        if (currentTime >= 6 && currentTime < 12) {
            setTime('morning')
        }
        if (currentTime >= 12 && currentTime < 18) {
            setTime('day')
        }
        if (currentTime >= 18 && currentTime < 24) {
            setTime('evening')
        }
    })



    return (
        <View style={styles.container}>
            <ImageBackground blurRadius={5} source={bgImage} style={styles.image} >
                <View style={styles.greeting}>
                    <Image source={avatar} style={styles.userAvatar} />
                    <View style={styles.greetingTextBlock}>
                        <Text style={styles.greetingText}>Good {time},</Text>
                        <Text onPress={() => navigation.navigate('SongsList')} style={styles.greetingText}>Macheloger!</Text>
                    </View>
                </View>
            </ImageBackground>
        </View>
    )

}

const styles = StyleSheet.create({
    container: {
        width: '100%',
        height: '100%',
        flex: 1,
    },
    image: {
        flex: 1,
        resizeMode: 'cover',
        justifyContent: 'center',
    },
    greeting: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
    },
    greetingTextBlock: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    greetingText: {
        color: 'white',
        fontSize: 24,
        fontFamily: 'Nunito-Bold',
        paddingVertical: 5
    },
    userAvatar: {
        width: 200,
        height: 200,
        borderRadius: 100,
        marginVertical: 60,
    }
})