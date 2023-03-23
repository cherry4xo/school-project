import React from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView } from 'react-native';

import { useNavigation } from '@react-navigation/native';
import { useState } from "react";
import { useEffect } from "react";
import { AlbumPageParams } from "../mobX/albumPage.js";

export default function AlbumComponent(props) {
    const navigation = useNavigation();
    const toAlbumPage = () => {
        AlbumPageParams.changeParams(props.id)

        AlbumPageParams.setLibraryTouchTrigger()

        navigation.navigate('LibraryPage')

        setTimeout(() => {
            navigation.navigate('LibraryPage', { screen: 'AlbumPage' })
        }, 1);
    }

    const [authors, setAuthors] = useState('')
    const [image, setImage] = useState(null)
    const getAlbumImage = async (id) => {
        try {
            let path = 'http://192.168.1.66:12345/album/get_picture/' + id
            const res = await fetch(
                path,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'image/*',
                        'Content-Type': 'image/*',
                    },
                    cache: 'no-cache'
                }
            );
            const imageBlob = await res.blob();
            const callback = URL.createObjectURL(imageBlob);
            return callback

        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        let string = ''
        for (let i = 0; i < props.authors.length; i++) {
            string += props.authors[i].name + ' '
        }
        setAuthors(string)
        const getImage = async () => {
            let img = await getAlbumImage(props.id)
            setImage(img)
        }
        getImage()
    }, [])

    return (
        <TouchableHighlight onPress={toAlbumPage}>
            <View style={{ width: 140, margin: 15 }}>
                <Image style={styles.container} source={{ uri: image }} />
                <Text
                    numberOfLines={1}
                    style={[styles.text, { maxWidth: 140, overflow: 'hidden', marginTop: 5 }]}>
                    {props.albumName}
                </Text>
                <Text
                    numberOfLines={1}
                    style={[styles.text, { fontSize: 16, color: '#FF0054', maxWidth: 140, overflow: 'hidden' }]}>
                    {authors}
                </Text>
            </View>
        </TouchableHighlight>

    );
}

const styles = StyleSheet.create({
    container: {
        borderRadius: 10,
        // backgroundColor: "#7cb48f", 
        borderColor: '#5A5A5A',
        borderWidth: 1,
        width: 'auto',
        height: 140,
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '18pt'
    },
})