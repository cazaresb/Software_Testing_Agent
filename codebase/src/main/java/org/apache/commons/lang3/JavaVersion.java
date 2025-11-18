/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.commons.lang3;

/**
 * <p>An enum representing all the versions of the Java specification.
 * This is intended to mirror available values from the
 * <em>java.specification.version</em> System property. </p>
 *
 * @since 3.0
 * @version $Id: $
 */
public enum JavaVersion {
    
    /**
     * The Java version reported by Android. This is not an official Java version number.
     */
    JAVA_0_9(1.5f, "0.9"),
    
    /**
     * Java 1.1.
     */
    JAVA_1_1(1.1f, "1.1"),

    /**
     * Java 1.2.
     */
    JAVA_1_2(1.2f, "1.2"),

    /**
     * Java 1.3.
     */
    JAVA_1_3(1.3f, "1.3"),

    /**
     * Java 1.4.
     */
    JAVA_1_4(1.4f, "1.4"),

    /**
     * Java 1.5.
     */
    JAVA_1_5(1.5f, "1.5"),

    /**
     * Java 1.6.
     */
    JAVA_1_6(1.6f, "1.6"),

    /**
     * Java 1.7.
     */
    JAVA_1_7(1.7f, "1.7"),

    /**
     * Java 1.8.
     */
    JAVA_1_8(1.8f, "1.8"),

    /**
     * Java 9.
     */
    JAVA_9(9.0f, "9"),

    /**
     * Java 10.
     */
    JAVA_10(10.0f, "10"),

    /**
     * Java 11.
     */
    JAVA_11(11.0f, "11"),

    /**
     * Java 12.
     */
    JAVA_12(12.0f, "12"),

    /**
     * Java 13.
     */
    JAVA_13(13.0f, "13"),

    /**
     * Java 14.
     */
    JAVA_14(14.0f, "14"),

    /**
     * Java 15.
     */
    JAVA_15(15.0f, "15"),

    /**
     * Java 16.
     */
    JAVA_16(16.0f, "16"),

    /**
     * Java 17.
     */
    JAVA_17(17.0f, "17");

    /**
     * The float value.
     */
    private float value;
    /**
     * The standard name.
     */
    private String name;

    /**
     * Constructor.
     *
     * @param value  the float value
     * @param name  the standard name, not null
     */
    JavaVersion(final float value, final String name) {
        this.value = value;
        this.name = name;
    }

    //-----------------------------------------------------------------------
    /**
     * <p>Whether this version of Java is at least the version of Java passed in.</p>
     *
     * <p>For example:<br />
     *  {@code myVersion.atLeast(JavaVersion.JAVA_1_4)}<p>
     *
     * @param requiredVersion  the version to check against, not null
     * @return true if this version is equal to or greater than the specified version
     */
    public boolean atLeast(final JavaVersion requiredVersion) {
        return this.value >= requiredVersion.value;
    }

    /**
     * Transforms the given string with a Java version number to the
     * corresponding constant of this enumeration class. This method is used
     * internally.
     *
     * @param nom the Java version as string
     * @return the corresponding enumeration constant or <b>null</b> if the
     * version is unknown
     */
    // helper for static importing
    static JavaVersion getJavaVersion(final String nom) {
        return get(nom);
    }

    /**
     * Transforms the given string with a Java version number to the
     * corresponding constant of this enumeration class. This method is used
     * internally.
     *
     * @param nom the Java version as string
     * @return the corresponding enumeration constant or <b>null</b> if the
     * version is unknown
     */
    static JavaVersion get(final String nom) {
        if ("0.9".equals(nom)) {
            return JAVA_0_9;
        } else if ("1.1".equals(nom)) {
            return JAVA_1_1;
        } else if ("1.2".equals(nom)) {
            return JAVA_1_2;
        } else if ("1.3".equals(nom)) {
            return JAVA_1_3;
        } else if ("1.4".equals(nom)) {
            return JAVA_1_4;
        } else if ("1.5".equals(nom)) {
            return JAVA_1_5;
        } else if ("1.6".equals(nom)) {
            return JAVA_1_6;
        } else if ("1.7".equals(nom)) {
            return JAVA_1_7;
        } else if ("1.8".equals(nom)) {
            return JAVA_1_8;
        } else if ("9".equals(nom) || (nom != null && nom.startsWith("9."))) {
            return JAVA_9;
        } else if ("10".equals(nom) || (nom != null && nom.startsWith("10."))) {
            return JAVA_10;
        } else if ("11".equals(nom) || (nom != null && nom.startsWith("11."))) {
            return JAVA_11;
        } else if ("12".equals(nom) || (nom != null && nom.startsWith("12."))) {
            return JAVA_12;
        } else if ("13".equals(nom) || (nom != null && nom.startsWith("13."))) {
            return JAVA_13;
        } else if ("14".equals(nom) || (nom != null && nom.startsWith("14."))) {
            return JAVA_14;
        } else if ("15".equals(nom) || (nom != null && nom.startsWith("15."))) {
            return JAVA_15;
        } else if ("16".equals(nom) || (nom != null && nom.startsWith("16."))) {
            return JAVA_16;
        } else if ("17".equals(nom) || (nom != null && nom.startsWith("17."))) {
            return JAVA_17;
        } else {
            // Try to handle numeric major versions like "9", "11.0.2" generically
            if (nom != null) {
                final String base = nom.contains(".") ? nom.substring(0, nom.indexOf('.')) : nom;
                try {
                    final int major = Integer.parseInt(base);
                    if (major >= 17) {
                        return JAVA_17;
                    } else if (major >= 16) {
                        return JAVA_16;
                    } else if (major >= 15) {
                        return JAVA_15;
                    } else if (major >= 14) {
                        return JAVA_14;
                    } else if (major >= 13) {
                        return JAVA_13;
                    } else if (major >= 12) {
                        return JAVA_12;
                    } else if (major >= 11) {
                        return JAVA_11;
                    } else if (major >= 10) {
                        return JAVA_10;
                    } else if (major >= 9) {
                        return JAVA_9;
                    }
                } catch (final NumberFormatException ex) {
                    // ignore and return null below
                }
            }
            return null;
        }
    }

    //-----------------------------------------------------------------------
    /**
     * <p>The string value is overridden to return the standard name.</p>
     *
     * <p>For example, <code>"1.5"</code>.</p>
     *
     * @return the name, not null
     */
    @Override
    public String toString() {
        return name;
    }

}
