import React from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView } from 'react-native';

export default function AlbumComponent(props) {
    return (
        <TouchableHighlight onPress={() => { }}>
            <View style={{ width: 140, margin: 15 }}>
                <Image style={styles.container} source={props.imagePath} />
                <Text
                    numberOfLines={1}
                    style={[styles.text, { maxWidth: 140, overflow: 'hidden' }]}>
                    {props.albumName}
                </Text>
                <Text
                    numberOfLines={1}
                    style={[styles.text, { fontSize: 16, color: 'grey', maxWidth: 140, overflow: 'hidden' }]}>
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
        borderWidth: 2,
        width: 'auto',
        height: 140,
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '18pt'
    },
})