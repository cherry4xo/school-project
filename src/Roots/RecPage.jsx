import React from 'react';
import { StyleSheet, Text, View, ScrollView } from 'react-native';

export default function RecPage({ navigation }) {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Rec page will be here...</Text>
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