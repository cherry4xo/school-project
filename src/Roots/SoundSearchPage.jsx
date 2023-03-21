import React from 'react';
import { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ActivityIndicator } from 'react-native';
import {
    MaterialIndicator,
    PulseIndicator,
} from 'react-native-indicators';

export default function SoundSearchPage({ navigation }) {

    const [loading, setLoading] = useState(false)

    async function search() {
        setLoading(true)
        setTimeout(() => {
            setLoading(false)
        }, 3000);
    }

    return (
        <View style={styles.container}>
            <Text style={[styles.text, { marginVertical: 25 }]}>Sound search page</Text>
            <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                <TouchableOpacity onPress={search} style={styles.searchButotn}>
                    <Text style={styles.text}>Find song</Text>
                </TouchableOpacity>
            </View>
            {
                loading ?
                    <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator trackWidth={10} size={220} color='#FF8C3E' />
                        </View>
                        {/* <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator size={220} color='blue' />
                        </View> */}
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator size={200} color='#FF5D3E' />
                        </View>
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <PulseIndicator size={300} color='#FF5D00' />
                        </View>
                    </View>
                    :
                    null
            }
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
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    },
    searchButotn: {
        width: 200,
        height: 200,
        borderRadius: 200 / 2,
        backgroundColor: '#FF0054',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    }
})