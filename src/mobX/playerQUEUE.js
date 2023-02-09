import { action, computed, makeObservable, observable } from "mobx"

class PlayerQueueMobx {
    currentTrack = 0
    queue = {
        "tracks": [
            {
                "artists": [
                    "Rammstein"
                ],
                "name": "Mein Hertz Brennt",
                "trackDuration": 98820,
                "trackPosition": 1,
                "route": require('../../assets/audio/Rammstein_-_Mein_Herz_brennt.mp3')
            },
            {
                "artists": [
                    "Rammstein"
                ],
                "name": "Adieu",
                "trackDuration": 126660,
                "trackPosition": 2,
                "route": require('../../assets/audio/Rammstein_-_Adieu.mp3')
            },
            {
                "artists": [
                    "Rammstein"
                ],
                "name": "Deutschland",
                "trackDuration": 98820,
                "trackPosition": 3,
                "route": require('../../assets/audio/Rammstein_-_DEUTSCHLAND_(musmore.com).mp3')
            },
        ]
    }

    constructor() {
        makeObservable(this, {
            queue: observable,
            changeQueue: action,
            getQueue: computed,
            currentTrack: observable,
            increaseCurrentTrack: action,
            decreaseCurrentTrack: action,
            getCurrentTrack: computed
        })
    }

    changeQueue(newQueue) {
        this.queue = newQueue
    }

    get getQueue() {
        return this.queue
    }

    increaseCurrentTrack = () => {
        if (this.currentTrack + 1 >= this.queue.tracks.length) {
            this.currentTrack = 0
        }
        else {
            this.currentTrack++
        }
    }

    decreaseCurrentTrack = () => {
        if (this.currentTrack - 1 < 0) {
            this.currentTrack = this.queue.tracks.length - 1
        } else {
            this.currentTrack--
        }
    }

    get getCurrentTrack() {
        return this.currentTrack
    }

}

export const PlayerQueue = new PlayerQueueMobx()