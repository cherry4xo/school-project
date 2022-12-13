import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default function LibrarySongs({ navigation }) {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Victory</Text>
        </View >
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
    },
    itemsPair: {
        display: 'flex',
        flexDirection: 'row',
    },
    menuItem: {
        width: 150,
        height: 150,
        borderRadius: 25,

        alignItems: 'center',
        justifyContent: 'center',

        margin: 8,
    }
})