import React from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView } from 'react-native';

import { useNavigation } from '@react-navigation/native';

export default function AlbumComponent(props) {
    const navigation = useNavigation();
    const toAlbumPage = () => navigation.navigate('AlbumPage')
    return (
        <TouchableHighlight onPress={toAlbumPage}>
            <View style={{ width: 140, margin: 15 }}>
                <Image style={styles.container} source={props.imagePath} />
                <Text
                    numberOfLines={1}
                    style={[styles.text, { maxWidth: 140, overflow: 'hidden', marginTop: 5 }]}>
                    {props.albumName}
                </Text>
                <Text
                    numberOfLines={1}
                    style={[styles.text, { fontSize: 16, color: '#FF0054', maxWidth: 140, overflow: 'hidden' }]}>
                    Author
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