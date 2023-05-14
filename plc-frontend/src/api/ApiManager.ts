import { IEffectData } from '../domainData/DomainData';

const handleErrors = (res: Response) => {
    if (!res.ok) {
        throw new Error(res.statusText)
    }
}

export const setEffect = async (effectData: IEffectData) => {
    const res = await fetch(`/effect/${effectData.effect}/${effectData.brightness}`, {
        method: "POST",
        mode: "same-origin",
        headers: {
            "Content-Type": "application/json"
        }
    })
    handleErrors(res)
    return res.json()
}

export const getStatus = async () => {
    const res = await fetch("/effect/current")
    handleErrors(res)
    return res.json()
}