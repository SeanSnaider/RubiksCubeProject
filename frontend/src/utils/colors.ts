/**
 * Sticker colors and human-readable names, shared by every cube view.
 *
 * A sticker's `Color` is the letter of the face it belongs to on a solved cube
 * (see `types/index.ts`). This module maps those letters to what the user
 * actually sees, so the 3D view, the 2D net and the solver's messages all agree
 * on which color is which.
 */
import type { Color, FaceName } from '../types'

/** Fill color for each sticker. Values match the original Pygame palette. */
export const STICKER_FILL: Record<Color, string> = {
    U: '#FFFFFF', // White
    D: '#FFFF00', // Yellow
    L: '#FFA500', // Orange
    R: '#FF0000', // Red
    F: '#00FF00', // Green
    B: '#0000FF', // Blue
}

/** Fill for a sticker that hasn't been given a color yet. */
export const BLANK_FILL = '#3a4a57'

/** Readable text color to draw on top of each sticker fill. */
export const STICKER_TEXT: Record<Color, string> = {
    U: '#000000',
    D: '#000000',
    L: '#000000',
    R: '#000000',
    F: '#000000',
    B: '#FFFFFF',
}

/** The color name a user would say for each sticker. */
export const COLOR_NAME: Record<Color, string> = {
    U: 'White',
    D: 'Yellow',
    L: 'Orange',
    R: 'Red',
    F: 'Green',
    B: 'Blue',
}

/** Where each face sits when the cube is held white-up, green-front. */
export const FACE_POSITION_NAME: Record<FaceName, string> = {
    U: 'Top',
    D: 'Bottom',
    L: 'Left',
    R: 'Right',
    F: 'Front',
    B: 'Back',
}

/** Every color, in the order the color picker shows them. */
export const ALL_COLORS: readonly Color[] = ['U', 'F', 'R', 'D', 'B', 'L']
