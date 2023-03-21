import React, { useEffect, useState } from "react";
import { Image, ImageBackground, View, Text, StyleSheet } from "react-native";

const bgImage = require('../../assets/img/HomeBG.png')
// const avatar = require('../../assets/img/avatar.jpg')

export default function HomePage({ navigation }) {

    const [time, setTime] = useState('')
    const [userName, setUserName] = useState(null)
    const [userAvatar, setUserAvatar] = useState(null)

    const getUserAvatar = async (id) => {
        try {
            let path = 'http://192.168.1.66:12345/user/get_picture/' + id
            const res = await fetch(
                path,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'image/*',
                        'Content-Type': 'image/*',
                    },
                }
            );
            const imageBlob = await res.blob();
            const callback = URL.createObjectURL(imageBlob);
            return callback

        } catch (error) {
            console.error(error);
        }
    };

    const getUserData = async (id) => {
        try {
            let path = 'http://192.168.1.66:12345/main?user_id=' + id
            const res = await fetch(
                path,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            );
            const json = await res.json();
            return json.user

        } catch (error) {
            console.error(error);
        }
    };

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

        const fetchUserData = async () => {
            let user = await getUserData(1)
            setUserName(user.name)
            let image = await getUserAvatar(1)
            setUserAvatar(image)
            console.log('start')
        }
        fetchUserData()
    }, [])



    return (
        <View style={styles.container}>
            <ImageBackground blurRadius={0} source={bgImage} style={styles.image}>
                <View style={styles.greeting}>
                    <Image source={{ uri: userAvatar }} style={styles.userAvatar} />
                    <View style={styles.greetingTextBlock}>
                        <Text style={styles.greetingText}>Good {time},</Text>
                        <Text style={[styles.greetingText, { color: '#FF0054' }]}>{userName}</Text>
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
        backgroundColor: 'black'
    }
})